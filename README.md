# Sports-Ontology

### Ontology classes structure

The diagram was built using [drawio](https://app.diagrams.net/). The file can be found under the /visualize directory, feel free to use it.


![Classes](../master/visualize/sports_ontology.png)


A full diagram with properties and data types was also built using [WebVOWL](http://www.visualdataweb.de/)
![Full](../master/visualize/sports_ontology_full.PNG)


### System requirements

Python 3.7+, Apache-jena-fuseki (see installatation steps below)

On Ubuntu 18.04 this means:
```shell
apt-get update -qq
apt-get install -qq build-essential virtualenv python3.7 python3.7-dev
```

### Python dependencies

```shell
virtualenv -p python3.7 .venv
.venv/bin/pip install -r requirements.txt
```

### Apache jena-fuseki

**Step1**: First of all, you need to download apache-jena and apache-jena-fuseki from [here](https://jena.apache.org/download/index.cgi). They contain both Windows and Linux running files.

**Step2**: Download the zip corresponding to each one of them and unpack the content to a separate folder.

**Step3**: Setup the environment for apache-jena. The Windows related files are on /bat, whereas the Linux related files are on /bin
On Linux / Mac
```
export JENA_HOME=the directory you downloaded Jena to
export PATH=$PATH:$JENA_HOME/bin
```
On Windows
```
SET JENA_HOME =the directory you downloaded Jena to
SET PATH=%PATH%;%JENA_HOME%\bat
```

**Step4**: Create a tdb database from the .owl file. You need to create an empty directory on your system (let's call it TDB_DIRECTORY)
Go to the apache-fuseki directory content and run:
On Linux / Mac
```
./tdbloader --loc TDB_DIRECTORY_PATH ontoly.owl_PATH
```
On Windows
```
.\tdbloader.bat --loc TDB_DIRECTORY_PATH ontoly.owl_PATH
```

**Step5**: Run fuseki server
Go to the apache-jena-fuseki directory content and run (ontology_name is whatever you want):
On Linux / Mac
```
./fuseki-server --loc=TDB_DIRECTORY_PATH \ontology_name
```
On Windows
```
.\fuseki-server.bat --loc=TDB_DIRECTORY_PATH \ontology_name
```

**Step6**: Go to localhost:3030 on any browser and enjoy your ontology.
