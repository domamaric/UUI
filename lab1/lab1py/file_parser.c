#include <stdio.h>
#include <string.h>

typedef void (*LineCallback)(const char *a, const char *b);

void read_file_line_by_line(const char *filename, LineCallback callback) {
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        perror("Error opening file\n");
        return;
    }

    char *line_buff = NULL;
    size_t line_size = 512;

    while (getline(&line_buff, &line_size, file) != -1) {
        // Remove newline character at the end of the line
        size_t len = strlen(line_buff);
        if (len > 0 && line_buff[len - 1] == '\n') {
            line_buff[len - 1] = '\0';
        }

        if (line_buff[0] == '#') continue;

        // Preprocess the string before passing it to the callback
        char *colon = strchr(line_buff, ':');
        if (colon != NULL) {
            *colon = '\0';  // Replace ':' with '\0' to split the string
            char *key = line_buff;
            char *values = colon + 2;

            // Call the callback function with the preprocessed line
            callback(key, values);
        }
    }

    fclose(file);
}