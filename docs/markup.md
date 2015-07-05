# Problem Statement
The task at our hands is to write a bunch of mantras. A mantra is series of
sanskrit words arranged in a set of lines. Usually 1, 2, or 4 etc.. Each mantra
has a process to invoke it with an appropriate pronunciation or metre.

We only worry about the writing part here.

# Content
There are two types of content.

## Verse
Each verse can be represented as a set of

* Sloka: the actual text of the verse
* Padachhed: the text broken into individual words
* Anvaya: the words arranged in a way to be meaningful

May be Sloka is restrictive. We should use Text, so that both prose and poems
can be covered. E.g. Geeta v/s Upanishads.

## Metadata
How are the metadata represented?

* in separate files per directory. E.g. Chapter name.
* in the content file itself. E.g. Translation, Language.

# Approaches
There are two ways to denote the markup language for the verses. We will
describe them in brief here in order to draw up a good comparison matrix.

## JSON
A json file can contain one or more instances of following:

    {
        "metadata": {},
        "content": [
            {
                "sloka": ["line1", "line2", "line3"],
                "padachhed": [["word1", "word2"], ["word2a", "word2b"], ["word3a"]],
                "anvaya": "word2a word1 word3a word2 word2b"
            }
        ]
    }

It will be easy to maintain an array of JSON objects in case there are multiple
slokas in a file.

For metadata file, the JSON object can look like:

    {
        "title": "Chapter 1"
    }

Every directory which wants a specific section maintains an `index.json` file.
The parser takes care of arranging the content in order of hierarchy.

## Markdown
A markdown file for a verse may be structured as

    <!-- Verse Metadata -->
    Key: Value

    <!-- Verse -->
    ~~~sloka
    line1
    line2
    line3
    ~~~

    ~~~padachhed
    word1 word2
    word2a word2b
    word3a
    ~~~

    ~~~anvaya
    word2a word1 word3a word2 word2b
    ~~~

The text at end of fencing block are the block identifiers. Each header must
specify what entity the content of it embodies. At the outset, three entity
types are supported: sloka, padachhed, anvaya.

Markdown provides an inherent support for additional `Key: Value` metadata
properties. They can be used for annotations like `Language`, `Date` etc..

It will be difficult to parse multiple slokas in a file. Each sloka has to be
identified with a number, OR parsing can always be in order - raise an error if
an `anvaya` appears without a parent `sloka`. This will not be supported in the
first iteration.

# Implementation
JSON representation will require the pelican-prajna plugin to read and render
content.

Key benefits of a markdown based markup is ease of authoring. Almost every
editor has a markdown mode, the user can grok the content and enhance it as
well.

JSON provides a way for machines to grok the content with ease. It is extensible
by design. Embedding other metadata will be easier in future.

Markdown implementation will require an extension for python-markdown to parse
the markdown content. May be it will not require any pelican work?

Prajna will support both markdown and json for the content authoring. Internally
we will convert markdown to json before we pass it on to static page writer.

## Choosing python-markdown vs commonmark
See (Spike on commonmarkdown)[https://gist.github.com/codito/c0e8af6a565f35298512]

During the spike, we realized the difficulty in extending python-markdown. It
provides a state based model, which is very generic (great!) but is costly to
start with. CommonMark though very strict in the representation, provides an AST
for the markup content out of the box.

We will use CommonMark to start with and later on consider python-markdown as
appropriate.
