## CLI download manager
Download files with multiple threads faster
> It needs to be free and safe right? use your own.
### Basic Usage
```
python main.py {URL} [OPTIONS]

[OPTIONS]
    --name {the name of the file}
        default - parse file name from url
    --num_threads {number of threads}
        default - 4

[Example]
    python main.py http://example.com --num_threads 8 --name hello.txt
```
### Note
Some type of url are not still working.
