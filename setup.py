import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__="0.0.0"

REPO_NAME = "Movie-Recommendation-System"
AUTHOR_USER_NAME = "Priyanshu Dey"
SRC_REPO = "Movie-Recommendation-System"
AUTHOR_EMAIL="priyanshudey.ds@gmail.com"
LIST_OF_REQUIREMENTS = ['streamlit', 'numpy']


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="It is a NLP Problem Statement",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/PriyanshuDey23/Movie-Recommendation-System",
    project_urls={
        "Bug Tracker":f"https://github.com/PriyanshuDey23/Movie-Recommendation-System/issues"
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src")

)