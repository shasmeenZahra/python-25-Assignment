import os
import streamlit as st

def rename_files(directory, prefix):
    try:
        files = os.listdir(directory)
        renamed_files = []
        
        for index, file in enumerate(files):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(file)[1]
                new_name = f"{prefix}_{index+1}{file_ext}"
                new_path = os.path.join(directory, new_name)
                os.rename(file_path, new_path)
                renamed_files.append((file, new_name))
        
        return renamed_files
    except Exception as e:
        return str(e)

st.title("Bulk File Renamer")

directory = st.text_input("Enter the directory path:")
prefix = st.text_input("Enter the file prefix:")

if st.button("Rename Files"):
    if directory and prefix:
        if os.path.exists(directory) and os.path.isdir(directory):
            renamed_files = rename_files(directory, prefix)
            if isinstance(renamed_files, str):
                st.error(f"Error: {renamed_files}")
            else:
                st.success("Bulk renaming completed successfully!")
                st.write("### Renamed Files:")
                for old_name, new_name in renamed_files:
                    st.write(f"{old_name} ➝ {new_name}")
        else:
            st.error("Invalid directory path. Please enter a valid folder path.")
    else:
        st.warning("Please enter both directory path and file prefix.")
