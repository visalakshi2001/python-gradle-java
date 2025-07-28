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
            wrapper = "./gradlew"
            shell_flag = False
        
        select_task = st.multiselect(
            "Select Task",
            ["clean", "build"],
            default=["clean", "build"],
            help="Select the Gradle task to run.",
        )
        cmd = [wrapper] + select_task
        st.write(f"Executable command: `{' '.join(cmd)}`")

        if st.button("Run Command", type="primary", icon="▶️"):
            with st.spinner("Running command..."):
                # Ensure the command is run in the project root directory
                if os.name == "nt":
                    cmd = " ".join(cmd)
                else:
                    cmd = " ".join([str(c) for c in cmd])
                proc = subprocess.run(
                    cmd,
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True
                )

            st.write("Command Output:")
            if proc.stdout:
                st.code(proc.stdout, language="bash")
            else:   
                st.write("No output from command.")



if __name__ == "__main__":
    main()