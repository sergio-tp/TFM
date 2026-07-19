CREATE TABLE month (
  idMonth NUMBER(10) NOT NULL,
  month NUMBER(10) NULL,
  year NUMBER(10) NULL,
  PRIMARY KEY (idMonth));


CREATE TABLE quarter (
  idQuarter NUMBER(10) NOT NULL,
  quarter NUMBER(10) NULL,
  year NUMBER(10) NULL,
  PRIMARY KEY (idQuarter));


CREATE TABLE location (
  idLocation NUMBER(10) NOT NULL,
  city VARCHAR2(45) NULL,
  region VARCHAR2(45) NULL,
  PRIMARY KEY (idLocation));


CREATE TABLE condition (
  idCondition NUMBER(10) NOT NULL,
  condition VARCHAR2(45) NULL,
  PRIMARY KEY (idCondition));


CREATE TABLE regime (
  idRegime NUMBER(10) NOT NULL,
  regime VARCHAR2(45) NULL,
  PRIMARY KEY (idRegime));


CREATE TABLE transactions (
  idTransaction NUMBER(10) NOT NULL,
  total_transactions NUMBER(10) NULL,
  total_transaction_price BINARY_DOUBLE NULL,
  quarter_idQuarter NUMBER(10) NOT NULL,
  location_idLocation NUMBER(10) NOT NULL,
  condition_idCondition NUMBER(10) NOT NULL,
  regime_idRegime NUMBER(10) NOT NULL,
  PRIMARY KEY (idTransaction, quarter_idQuarter, location_idLocation, condition_idCondition, regime_idRegime),
  CONSTRAINT fk_transactions_quarter
    FOREIGN KEY (quarter_idQuarter)
    REFERENCES quarter (idQuarter),
  CONSTRAINT fk_transactions_location
    FOREIGN KEY (location_idLocation)
    REFERENCES location (idLocation),
  CONSTRAINT fk_transactions_condition
    FOREIGN KEY (condition_idCondition)
    REFERENCES condition (idCondition),
  CONSTRAINT fk_transactions_regime
    FOREIGN KEY (regime_idRegime)
    REFERENCES regime (idRegime));


CREATE TABLE sales (
  idSale NUMBER(10) NOT NULL,
  total_sales NUMBER(10) NULL,
  month_idMonth NUMBER(10) NOT NULL,
  location_idLocation NUMBER(10) NOT NULL,
  condition_idCondition NUMBER(10) NOT NULL,
  regime_idRegime NUMBER(10) NOT NULL,
  PRIMARY KEY (idSale, month_idMonth, location_idLocation, condition_idCondition, regime_idRegime),
  CONSTRAINT fk_sales_month
    FOREIGN KEY (month_idMonth)
    REFERENCES month (idMonth),
  CONSTRAINT fk_sales_location
    FOREIGN KEY (location_idLocation)
    REFERENCES location (idLocation),
  CONSTRAINT fk_sales_condition
    FOREIGN KEY (condition_idCondition)
    REFERENCES condition (idCondition),
  CONSTRAINT fk_sales_regime
    FOREIGN KEY (regime_idRegime)
    REFERENCES regime (idRegime));


CREATE TABLE appraisals (
  idAppraisal NUMBER(10) NOT NULL,
  average_appraised_price_m2 BINARY_DOUBLE NULL,
  quarter_idQuarter NUMBER(10) NOT NULL,
  location_idLocation NUMBER(10) NOT NULL,
  PRIMARY KEY (idAppraisal, quarter_idQuarter, location_idLocation),
  CONSTRAINT fk_appraisals_quarter
    FOREIGN KEY (quarter_idQuarter)
    REFERENCES quarter (idQuarter),
  CONSTRAINT fk_appraisals_location
    FOREIGN KEY (location_idLocation)
    REFERENCES location (idLocation));