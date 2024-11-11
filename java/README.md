# AGI Java

Application suite to connect to Agenzia delle Entrate.

- accounting: fatture elettroniche

## Build and Run

You can create the packages as follows

```bash
# both jars
mvn clean package
# only macos
mvn clean package -P macos
# only windows
mvn clean package -P windows
```

## Run 

Once you have the packages, just run them on your system

```bash
cd java/accounting/target
java -XstartOnFirstThread -jar target/my-swt-app-1.0-SNAPSHOT-mac-jar-with-dependencies.jar
```

## Dev Run

You can also run your application from maven, using: 

```bash
# on mac
mvn exec:java -P macos

# on win
mvn exec:java -P windows
```