# %% Import packages
from projects.example.demo import project_specific_function
from shared.config import config


# %% Main function
def main():
    print(config.paths.outputs)
    print(config.paths.working)
    print("----")
    print(config.aws.access_key_id)

    project_specific_function()


# %% This is executed when run from the command line
if __name__ == "__main__":
    main()
