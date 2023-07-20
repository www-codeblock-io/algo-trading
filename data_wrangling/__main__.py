from data_wrangling import ingestion, cleaning, transformation, feature_engineering


def main():
    # Ingest data using the ingestion module
    raw_data = ingestion.load_data('data.csv')

    # Clean the data using the cleaning module
    clean_data = cleaning.clean(raw_data)

    # Perform transformations using the transformation module
    transformed_data = transformation.transform(clean_data)

    # Analyze the data using the analysis module
    results = feature_engineering.analyze(transformed_data)

    # Output the results
    print(results)


if __name__ == '__main__':
    main()

