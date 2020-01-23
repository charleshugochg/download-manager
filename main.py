import click

from downloader import DownloadManager, parse_filename
from filemanager import DownloadFile
from printer import OneLinePrinter
from progressbar import ProgressBarFormatter


def on_chunk(pointer, chunk, params):
    bar, fp, *_ = params
    fp.seek(pointer)
    fp.write(chunk)
    bar.update_increment(len(chunk))


@click.command(help="It downloads the specified file with specified name")
@click.option('--num_threads', default=4, help="Number of Threads")
@click.option('--name', type=click.Path(), help="Name of the file with extension")
@click.argument('url', type=click.Path())
@click.pass_context
def main(ctx, url, name, num_threads):
    num_downloads = num_threads
    url = url
    file_name = name
    if not file_name:
        file_name = parse_filename(url)

    with OneLinePrinter("Initializing..."):
        manager = DownloadManager(url)
        manager.create_downloads(num_downloads)

    file_size = manager.size

    formatter = ProgressBarFormatter('Downloading')
    with OneLinePrinter(formatter):
        with DownloadFile(file_name, file_size) as f:
            for download in manager.iter_downloads():
                b = formatter.create_bar(download.length)
                formatter.add_bar(b)
                download.bind(on_chunk, b, f)
                download.start()
            for download in manager.iter_downloads():
                download.join()


if __name__ == '__main__':
    main(obj={})

