import streamlit as st
import subprocess
import os
from pathlib import Path

st.set_page_config(
    page_title="Print Output",
    page_icon=":printer:",
    layout="wide",
)


def main():

    PROJECT_ROOT = Path(__file__).parent.resolve()

    st.write(f"subprocess runs on {PROJECT_ROOT}")

    uploaded_oml = st.file_uploader(
        "Upload OML File",
        type=["oml"],
        help="Upload an OML file to visualize the print output.",
    )

    if uploaded_oml:
        st.write(f"OS Found: {os.name}")
        if os.name == "nt":  # Windows
            wrapper = "gradlew.bat"
            # On Windows it’s often simpler to run under shell so the .bat is recognized
            shell_flag = True
        else:
            # For Unix-like systems, use the gradlew script directly
            # Build the command such that permissions will not be an issue
            wrapper = str(PROJECT_ROOT / "gradlew")
            # Ensure the script is executable


            shell_flag = False
        
        select_task = st.multiselect(
            "Select Task",
            ["clean", "build", "tasks"],
            default=["clean", "build"],
            help="Select the Gradle task to run.",
        )
        cmd = [wrapper] + select_task
        st.write(f"Executable command: `{' '.join(cmd)}`")

        if st.button("Run Command", type="primary", icon="▶️"):
            with st.spinner("Running command..."):
                proc = subprocess.run(
                    cmd,
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=shell_flag
                )

            st.write("Command Output:")
            if proc.stdout:
                st.code(proc.stdout, language="bash")
            else:   
                st.write("No output from command.")



if __name__ == "__main__":
    main()