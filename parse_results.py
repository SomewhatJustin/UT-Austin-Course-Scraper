import csv


def parse_results(csv_file_path, output_csv_file_path):
    """
    Parse each line of the CSV file, split the course into two parts at the first period,
    and write the results to a new CSV file.
    :param csv_file_path: Path to the input CSV file.
    :param output_csv_file_path: Path to the output CSV file.
    """
    with open(csv_file_path, "r", newline="", encoding="utf-8") as infile, open(
        output_csv_file_path, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

        # Writing headers for the new CSV file
        writer.writerow(["Course Code", "Course Name", "Description"])

        for row in reader:
            # Assuming the row format is [Course, Description]
            course, description = row

            # Splitting the course at the first period
            if "." in course:
                course_code, course_name = course.split(".", 1)
            else:
                course_code, course_name = course, ""

            # Writing the new row to the output file
            writer.writerow([course_code.strip(), course_name.strip(), description])


# Usage
parse_results("output.csv", "output-parsed.csv")
