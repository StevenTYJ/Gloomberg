
###########################PART1 AUM Processing################################

import pandas as pd
from openpyxl import load_workbook, Workbook
pd.options.display.float_format = '{:.6f}'.format
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# Specify the path to your spreadsheet file
file_path = r'C:\Users\T\Desktop\OneRiver\ORAM-Input.xlsx'
# Read the spreadsheet
excel_data = pd.ExcelFile(file_path)  # For .xlsx files
# data = pd.read_csv(file_path)  # Use this for .csv files



Weight= excel_data.parse("Weight")
allocation_data = excel_data.parse("Allocation")
pnl_data = excel_data.parse("PnL by Asset Class")
aum_data= excel_data.parse("BOM AUM")

aum_data = aum_data.rename(columns={'BOM AUM': 'Allocation'})  # Rename column for consistency
allocation_data = pd.concat([aum_data, allocation_data])  # Concatenate the datasets

# Sort by Date
allocation_data['Date'] = pd.to_datetime(allocation_data['Date'])
allocation_data = allocation_data.sort_values(by='Date').reset_index(drop=True)

# Calculate cumulative AUM
allocation_data['Cumulative AUM'] = allocation_data['Allocation'].cumsum()

allocation_data = pd.DataFrame(allocation_data)
allocation_data = allocation_data.drop(columns=['Allocation'])

###########################PART2 Return Calculation################################

# Convert to DataFrames
allocation_df = pd.DataFrame(allocation_data)
pnl_df_updated = pd.DataFrame(pnl_data)


# Convert 'Date' column to datetime format
allocation_df['Date'] = pd.to_datetime(allocation_df['Date'])
pnl_df_updated['Date'] = pd.to_datetime(pnl_df_updated['Date'])

# Merge both dataframes on 'Date'
merged_df_updated = pd.merge(pnl_df_updated, allocation_df, on='Date', how='outer')
# Forward fill AUM to account for changes within the month
merged_df_updated['Cumulative AUM'] = merged_df_updated['Cumulative AUM'].ffill()
merged_df_updated['Cumulative AUM'] = merged_df_updated['Cumulative AUM'].bfill()
# Perform an merge to get the nearest percentage based on date and asset class
merged_df_updated = pd.merge_asof(merged_df_updated, Weight, left_on='Date', right_on='Date', left_by='Asset Class', right_by='Asset Class')

###########################PART2 Return Calculation###############################

merged_df_updated['Underlying asset'] = merged_df_updated['Cumulative AUM'] * merged_df_updated['Weight']
merged_df_updated['Daily Return'] = merged_df_updated['Daily PnL'] / merged_df_updated['Underlying asset']
merged_df_updated['Year-Month'] = merged_df_updated['Date'].dt.to_period('M')
merged_df_updated['Weighted Return'] = merged_df_updated['Daily Return'] * merged_df_updated['Weight']
monthly_return_per_asset = merged_df_updated.groupby(['Year-Month', 'Asset Class'])['Weighted Return'].apply(lambda x: (1 + x).prod() - 1)





# merged_df_updated['Underlying asset'] = merged_df_updated['Cumulative AUM'] * merged_df_updated['Weight']
# merged_df_updated['Daily Return'] = merged_df_updated['Daily PnL'] / merged_df_updated['Underlying asset']
# merged_df_updated['Year-Month'] = merged_df_updated['Date'].dt.to_period('M')

print(monthly_return_per_asset)


###################################
# Calculate monthly return for each asset class separately by Year-Month
# monthly_return_per_asset = merged_df_updated.groupby(['Year-Month', 'Asset Class'])['Daily Return'].apply(lambda x: (1 + x).prod() - 1)
# daily_return_per_asset = merged_df_updated.groupby(['Date', 'Asset Class'])['Daily Return'].apply(lambda x: (1 + x).prod() - 1).reset_index()
###########################################



# Display the monthly return for each asset class by month

# monthly_return_per_asset_df= monthly_return_per_asset.reset_index()
# monthly_return_per_asset_df.columns = ['Year-Month', 'Asset Class', 'Monthly Return']
# # Calculate overall monthly return for each month
#
# monthly_returns = monthly_return_per_asset_df.groupby('Year-Month')['Monthly Return'].sum().reset_index()

# Display the results
