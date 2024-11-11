# AGI Java Accounting

Application to connect to Aegnzia delle entrate

Accounting for "fattura elettronica"

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

You can run as follows

On Mac
```bash
java -XstartOnFirstThread -jar target/accounting-macos-0.0.1-SNAPSHOT-jar-with-dependencies.jar
```

On Windows
```bash
java -jar target/accounting-windows-0.0.1-SNAPSHOT-jar-with-dependencies.jar
```