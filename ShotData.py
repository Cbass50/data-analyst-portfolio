import pandas as pd

# Load the play-by-play data
pbp_data = pd.read_csv('pbp.csv')

#Display first few rows of the data
# print(pbp_data.head())

# Filter data to only include shot attempts

shot_data = pbp_data[(pbp_data['type'] == 'Made Shot') | (pbp_data['type'] == 'Missed Shot')]

# Group by player and shot subtype, then calculate FG%
fg_percentage = shot_data.groupby(['player', 'playerid','subtype' ]).apply(
    lambda group: pd.Series({
        'Shots Made': (group['result'] == 'Made').sum(),
        'Total Shots': group.shape[0],
        'FG%': ((group['result'] == 'Made').sum() / group.shape[0]) * 100
    })
).reset_index()
print(fg_percentage.head())

# 1. Calculate the average FG% for each shot subtype
avg_fg_percentage = fg_percentage.groupby('subtype')['FG%'].mean().reset_index()
avg_fg_percentage = avg_fg_percentage.rename(columns={'FG%': 'Average FG%'})

# 2. Merge the average FG% with the original fg_percentage DataFrame
merged_data = fg_percentage.merge(avg_fg_percentage, on='subtype', how='left')

# 3. Calculate the difference in FG%
merged_data['FG% Difference'] = merged_data['FG%'] - merged_data['Average FG%']

merged_data.to_csv('merged_data.csv')