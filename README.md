### Data Structures (SOC 2010)
# Reach Destination in the Fastest Way

---
Manual on usage of the Application developed during the Data Structures Major Assignment.

Application finds for you the shortest path between two specified locations.

---
### Before You Start

Ensure that you have already installed all requirements listed in *requirements.txt* and have stable internet connection

If have not installed yet, run following command:

```shell
pip install -r requirements.txt
```

*Also, it is highly recommended to use local virtual environments*

To create local virtual environment, run following commands in your terminal:

```shell
pip install virtualenv

# Test your installation:
virtualenv --version

virtualenv venv  # or any other name instead of venv

source venv/Scripts/activate
```

**Note** that last command `source venv/Scripts/activate` is only for Mac/Linux systems. If you use Windows Powershell execute `./venv/Scripts/activate` instead

---
### Running the App

1. Navigate to your project directory using `cd` command
2. Execute `python main.py`
3. Input your starting point name and destination point
4. Program will automatically generate path and open OpenStreetMap based map in your default browser

*E.g.:*
``` yaml
<< Enter name of origin place:
>> Inha University in Tashkent
<< Enter name of destination place:
>> Chilonzor 9 mavzesi
<< Gathering fresh datasets...:
<< Searching for shortest route...:
```
