from flask import Flask, make_response, request
import os
import io
import csv

app = Flask(__name__)


def split_csv(source_filepath, dest_folder, split_file_prefix, records_per_file):
    """
    Split a source csv into multiple csvs of equal numbers of records,
    except the last file.

    Includes the initial header row in each split file.

    Split files follow a zero-index sequential naming convention like so:

        `{split_file_prefix}_0.csv`
    """
    if records_per_file <= 0:
        raise Exception("records_per_file must be > 0")

    with open(source_filepath, "r") as source:
        reader = csv.reader(source)
        headers = next(reader)

        file_idx = 0
        records_exist = True

        while records_exist:

            i = 0
            target_filename = f"{split_file_prefix}_{file_idx}.csv"
            target_filepath = os.path.join(dest_folder, target_filename)

            with open(target_filepath, "w") as target:
                writer = csv.writer(target)

                while i < records_per_file:
                    if i == 0:
                        writer.writerow(headers)

                    try:
                        writer.writerow(next(reader))
                        i += 1
                    except StopIteration:
                        records_exist = False
                        break

            if i == 0:
                # we only wrote the header, so delete that file
                os.remove(target_filepath)

            file_idx += 1


@app.route("/")
def form():
    return """
        <html>
            <body>
                <h1>Transform a file demo</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """


@app.route("/transform", methods=["POST"])
def transform_view():
    split_file_prefix = "split_file"
    dest_folder = os.path.abspath(os.getcwd())

    f = request.files["data_file"]
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    headers = next(csv_input)
    file_idx = 0
    records_exist = True

    while records_exist:
        i = 0
        target_filename = f"{split_file_prefix}_{file_idx}.csv"
        target_filepath = os.path.join(dest_folder, target_filename)

        with open(target_filepath, "w") as target:
            writer = csv.writer(target)

            while i < 1000:
                if i == 0:
                    writer.writerow(headers)

                try:
                    writer.writerow(next(csv_input))
                    i += 1
                except StopIteration:
                    records_exist = False
                    break

        if i == 0:
            # we only wrote the header, so delete that file
            os.remove(target_filepath)

            file_idx += 1

    return 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
