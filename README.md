#  Unit Testing of writing
    If you annotate sections of text with meta-data, you can unit test that text to fulfill particular conditions.

## Architecture Design 
    Python + nlp to generate the document structure,
    write a little unit test framework to test the produced structures.

### Libraries:
    Spacy, pyparsing

## Annotations in the text:
    Use something not likely to be in the written document to begin with.. 
    %tag% may be best?
    Have a pre-processor to:
        import other files
        group text into data structures of (tags, [text/subdocuments])
    Have a processor to strip tags for export,
        
    Recognise references (a..., 93)
    headings, org style: ** Blah
    


## Things you could test for:
    document structure:
        headings
        subsections
        titles
        lists
        image references
        
    
    tags { argument, structural, etc }
    regexs
    references:
        amount
        colocation ( eg: mention(fligstein).with(bourdieu)
    structure ordering
    size:
        wordcount
        sentence length
        paragraph leng
    


## Examples (using Chai-style notation):
   document.should.have.a.section('background')
   document.should.mention('fligstein')
   document.section('background').should.mention('bourdieu')
   document.should.have.a.length.larger.than(10).pages
   
   document.section('introduction').should.precede.section('background')
   document.section('introduction').should.mention('research questions')
   document.section('introduction').should.have.subsections(3)
