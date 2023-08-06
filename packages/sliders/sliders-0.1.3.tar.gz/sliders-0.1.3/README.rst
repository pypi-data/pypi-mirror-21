Sliders
-------

Currently only includes one module: flextableparser. To use::

    >>> from sliders import flextableparser
    >>> parser = flextableparser.FlexTableParser(config.json, output_file, static_values)
    >>> parser = flextableparser.FlexTableParser()
    >>> parser.configure(json_file)
    >>> parser.add_static_values(dict)
    >>> parser.parse_file(input_file, output_file_handle)
    >>> output = parser.parse_file(input_file)

    $ text2table --schema=fastqc fastqc.data
    $ text2table --schema=fastqc fastqc.data 2>&1 > fastqc.csv  # Send CSV output to file
    $ text2table --schema=fastqc fastqc_1.data fastqc_2.data
    $ text2table --schema=fastqc --output_file=out.csv fastqc.data
    $ text2table --schema=fastqc --output_file=out.csv --static_values=series:test,sample:A fastqc.data
    $ text2table --schema=fastqc ../tests/sample_fastqc.data ../tests/sample_fastqc_2.data 2>&1 >/dev/null