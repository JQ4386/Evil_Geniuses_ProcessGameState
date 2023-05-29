import numpy as np

import pandas as pd

import pyarrow.parquet as pq

import matplotlib.path as path

import matplotlib.pyplot as plt

import seaborn as sns

'''
External Python Libraries used include matplotlib, pandas and seaborn. These libraries make the data processing steps much simpler (to implement and to read) and enable the data be to efficently visualized. 
'''

class ProcessGameState:
    '''
    Creates a gamedata processor based off a parquet file, with different functionalities based on assignment requirements. 
            
        1b) - Each row is tested to see if the location lies within the specified chokepoint (light blue region).     
        1c) - The weapon_class was extracted from the inventory column of the data file.
        2a) - Returns a dataframe which provides insight on whether passing through a specified chokepoint is a common strategy for a Team on a certain side. 
        2b) - Returns a float value for the average timer for Team2 to enter BombsiteB with at least 2 Rifles or SMGs
        2c) - Outputs a KDE Jointplot on the standing position of Team2's CT players inside BombsiteB.
            
    *The functions were not implemented for general use (only used to answer the specific questions), but can easily be generalized to accept different inputs by replacing variables like column titles with local variables.
    '''
    
    def __init__(self, path_to_parquet, vertices, z_range):
        '''
        Parameters:
        ----------
        path_to_parquet : str
            The file path to the parquet file. This file will be parsed and used as dataset in the class.
        vertices : list
            List of tuples which contain the coordinates of the specified choke-point (light blue area in the assignment)
        z_range : tuple
            Tuple which contains the minimum and maximum (inclusive) z-values of the specified area.
        '''
        
        #Parse the parquet file and convert into dataframe
        self.df = pd.read_parquet(path_to_parquet)
        self.area = path.Path(vertices=vertices)
        self.z_range = z_range
        self._preprocess()

    def _preprocess(self):
        '''
        Simple processing to perform some calculations and to append relevant data to the main dataframe.
            'is_inside' (boolean) is determined using the .is_inside_polygon method, which uses odd/even raycasting and runs in O(V) time (where V is the number of vertices of the specified region). As V is usually a relatively small number, this is trivial in most cases (practically equivalent to O(1)), but can increase if the number of vertices in the region rises significantly. This data is appended to the main dataframe. Used for 1b).
            'weapon_classes' (list) is determined by applying a lambda function to extract the 'weapon_class' information from the 'inventory column'. This data is appended to the main dataframe. Used for 1c) and 2b).
            'has_rifle_or_smg' (boolean) is determined by applying a lambda function to examine if 'Rifle' or 'SMG' appears in the 'weapon_classes' column. Used for 2b).
        '''
        def is_inside_polygon(row):
            '''
            helper function
            '''
            point = (row['x'], row['y'])
            return self.area.contains_point(point) & (row['z'] >= self.z_range[0]) & (row['z'] <= self.z_range[1]) 
        
        self.df['is_inside'] = self.df.apply(is_inside_polygon, axis=1)
        weapon_classes = self.df['inventory'].apply(lambda x: [item['weapon_class'] for item in x] if x is not None else [])
        self.df['weapon_classes'] = weapon_classes
        self.df['has_rifle_or_smg'] = self.df['weapon_classes'].apply(lambda x: 'Rifle' in x or 'SMG' in x)
        
    #Solutions for Q2a) and Q2b) are added as methods in the class, but can be generalized to take variable inputs.

    def question_2a(self):
        #Filters the dataframe to only include players who are on Team2 playing as T and is inside the chokepoint. 
        Team2TInside = self.df[(self.df['is_inside'] == True) & (self.df['team'] == 'Team2') & (self.df['side'] == 'T')]
        
        #Duplicate values of same players in the same round are dropped (as they do not provide information on whether the team entered via the chokepoint that round)
        subset = Team2TInside.drop_duplicates(subset=['round_num', 'player'])
        print(subset)
        print('According to the results, Team2 only entered the light blue region as T for 1 round, and only 2 players entered that region for that round (r16). As such, it is safe to conclude that entering via the light blue region is not a common strategy employed by Team2 on side T.')
        return subset

    def question_2b(self):
        #Filters the dataframe to only includes players who are on Team2 playing as T, is inside BombsiteB and has either a Rifle or a SMG in their inventory 
        df_filtered = self.df[(self.df['team'] == 'Team2') & (self.df['side'] == 'T') & (self.df['area_name'] == 'BombsiteB') & (self.df['has_rifle_or_smg'] == True)]
        df_filtered = df_filtered.sort_values('tick')
        
        # Helper function to determine the timer (seconds) where at least two such players first enter into the bombsite
        def get_tick_two_players(group):
                player_entries = group.drop_duplicates(subset='player')
                if len(player_entries) >= 2:
                    return player_entries.reset_index().at[1, 'seconds'] 
                else:
                    return None

        #Groupby the filtered data according to the round number to get the time the specificed event took place for each round, then get the mean value of those rounds 
        meanTimer = df_filtered.groupby('round_num').apply(get_tick_two_players).mean()
        print(f'average timer that Team2 on T (terrorist) side enters “BombsiteB” with least 2 rifles or SMGs is {meanTimer} seconds.')
        return meanTimer

        
    def create_heatmap(self):
        '''
        A KDE (Kernel Density Estimation) jointplot was chosen here instead of a regular heatmap/kdeplot to give an additional axes-specific representation of the distribution of player locations. This provides valuable insight on angle-based tactics such as peaking, hard-scoping, sniping etc.
        sns (seaborn) is used here because it has signifcantly optimized performance compared to other methods e.g. scipy.stats.gaussian_kde.
        '''
        
        #Filters the dataframe to only includes players who are on Team2 playing as CT and is inside BombsiteB 
        df_filtered = self.df[(self.df['team']=='Team2') & (self.df['side']=='CT') & (self.df['area_name']=='BombsiteB') & (self.df['is_alive'] == True)]
        
        #Creates a kde jointplot (as a heatmap) 
        heatmap = sns.jointplot(data=df_filtered, x = 'x', y='y', kind='kde', cmap='OrRd', fill=True, color='orange')
        heatmap.set_axis_labels('X-Coordinate', 'Y-Coordinate')
        heatmap.fig.suptitle('KDE Heatmap of BombsiteB')
        plt.show()
        
#Input Variables From Assignment
vertices = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
z_range = (285, 421)
path_to_parquet = '/Users/jq4386/Desktop/Evil Geniuses /game_state_frame_data.parquet'

#Output
Output = ProcessGameState(path_to_parquet, vertices, z_range)
Output.question_2a()
Output.question_2b()
#Question 2c)
Output.create_heatmap()
        
        
                