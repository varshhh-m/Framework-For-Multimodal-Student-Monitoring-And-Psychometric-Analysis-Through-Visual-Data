import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load Excel file and return a list of sheet names
def load_excel(file_path):
    xl = pd.ExcelFile(file_path)
    return xl.sheet_names

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to plot bar plot based on selected sheet
def plot_bar_plot(df, sheet_name):
    selected_sheet = df[sheet_name]
    selected_sheet.set_index(selected_sheet.columns[0], inplace=True)
    selected_sheet.plot(kind='bar')
    plt.xlabel(selected_sheet.columns[0])
    plt.ylabel('Values')
    plt.title(f'Bar Plot for {sheet_name}')
    st.pyplot()

# Main function
def main():
    st.title('Excel Sheet Visualizer')

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name=None)

        # Get sheet names
        sheet_names = load_excel(uploaded_file)

        # Dropdown to select sheet
        selected_sheet = st.selectbox("Select Sheet", sheet_names)

        # Plot bar plot based on selected sheet
        plot_bar_plot(df, selected_sheet)

# Run the app
if __name__ == "__main__":
    main()
