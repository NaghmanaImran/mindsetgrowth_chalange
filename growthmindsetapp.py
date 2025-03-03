import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image
import PyPDF2

def main():
    st.title("Growth Mindset Data Assistant 📈")
    st.sidebar.header("Navigation")
    
    menu = ["Data Upload & Clean", "Visualization", "File Management"]
    choice = st.sidebar.selectbox("Choose Operation", menu)
    
    if choice == "Data Upload & Clean":
        data_cleaning_section()
    elif choice == "Visualization":
        visualization_section()
    elif choice == "File Management":
        file_management_section()

def data_cleaning_section():
    st.header("Data Upload & Cleaning 🧹")
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Original Data Preview:")
        st.dataframe(df.head())
        
        # Cleaning options
        st.subheader("Cleaning Options")
        
        # Remove duplicates
        if st.checkbox("Remove duplicate rows"):
            df = df.drop_duplicates()
            st.success("Duplicates removed!")
        
        # Handle missing values
        if st.checkbox("Handle missing values"):
            missing_strategy = st.selectbox(
                "Choose strategy for missing values",
                ["Drop rows", "Fill with mean", "Fill with median", "Fill with zero"]
            )
            
            if missing_strategy == "Drop rows":
                df = df.dropna()
            elif missing_strategy == "Fill with mean":
                df = df.fillna(df.mean())
            elif missing_strategy == "Fill with median":
                df = df.fillna(df.median())
            elif missing_strategy == "Fill with zero":
                df = df.fillna(0)
            
            st.success("Missing values handled!")
        
        # Download cleaned data
        if st.button("Download Cleaned Data"):
            csv = df.to_csv(index=False)
            b64 = io.BytesIO()
            b64.write(csv.encode())
            st.download_button(
                label="Download CSV",
                data=b64.getvalue(),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

def visualization_section():
    st.header("Data Visualization 📊")
    uploaded_file = st.file_uploader("Upload your CSV file for visualization", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Select columns for visualization
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_columns) > 0:
            st.subheader("Create Visualizations")
            plot_type = st.selectbox(
                "Choose plot type",
                ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Box Plot"]
            )
            
            selected_column = st.selectbox("Select column to visualize", numeric_columns)
            
            fig, ax = plt.subplots()
            
            if plot_type == "Line Plot":
                plt.plot(df[selected_column])
            elif plot_type == "Bar Plot":
                plt.bar(range(len(df[selected_column])), df[selected_column])
            elif plot_type == "Scatter Plot":
                plt.scatter(range(len(df[selected_column])), df[selected_column])
            elif plot_type == "Histogram":
                plt.hist(df[selected_column])
            elif plot_type == "Box Plot":
                plt.boxplot(df[selected_column])
            
            plt.title(f"{plot_type} of {selected_column}")
            st.pyplot(fig)
            
            # Save plot option
            if st.button("Save Plot"):
                plt.savefig("plot.png")
                st.success("Plot saved as 'plot.png'!")
        else:
            st.warning("No numeric columns found in the dataset!")

def file_management_section():
    st.header("File Management 📁")
    
    # File removal section
    st.subheader("Remove Files")
    file_to_remove = st.file_uploader("Select file to remove", type=['csv', 'pdf'])
    
    if file_to_remove is not None:
        if st.button("Remove File"):
            # Here we're just clearing the file from the uploader
            # In a real application, you'd need to implement actual file deletion
            st.success(f"File {file_to_remove.name} would be removed!")
    
    # PDF handling section
    st.subheader("PDF Operations")
    pdf_file = st.file_uploader("Upload PDF file", type=['pdf'])
    
    if pdf_file is not None:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        st.write(f"Number of pages: {num_pages}")
        
        # Display PDF content
        page_num = st.number_input("Enter page number to view", min_value=1, max_value=num_pages, value=1)
        page = pdf_reader.pages[page_num-1]
        st.text(page.extract_text())

if __name__ == "__main__":
    main()
