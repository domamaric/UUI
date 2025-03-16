#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define ANSI_RED "\x1b[31m"
#define ANSI_RESET "\x1b[0m"

typedef void (*LineCallback)(const char *state, const char *next_state, int cost);

void read_file_line_by_line(const char *filename, LineCallback callback)
{
        FILE *file = fopen(filename, "r");

        if (file == NULL)
        {
                perror("[" ANSI_RED "ERROR" ANSI_RESET "] Cannot open file");
                exit(EXIT_FAILURE);
        }

        char *line_buff = NULL;
        size_t line_size = 0;

        while (getline(&line_buff, &line_size, file) != -1)
        {
                // Remove newline character
                size_t len = strlen(line_buff);

                if (len > 0 && line_buff[len - 1] == '\n')
                        line_buff[len - 1] = '\0';

                if (line_buff[0] == '#')
                        continue; // Skip comments

                // Find the separator (": ")
                char *colon = strchr(line_buff, ':');

                if (colon != NULL)
                {
                        *colon = '\0'; // Split the string at ':'
                        char *state = line_buff;
                        char *successors = colon + 2; // Skip ": "

                        // Now split each "next_state,cost" pair
                        char *token = strtok(successors, " ");
                        while (token)
                        {
                                char *comma = strchr(token, ',');
                                if (comma)
                                {
                                        *comma = '\0'; // Split at comma
                                        char *next_state = token;
                                        int cost = atoi(comma + 1);

                                        // Send each pair separately
                                        callback(state, next_state, cost);
                                }
                                token = strtok(NULL, " ");
                        }
                }
        }

        fclose(file);
        free(line_buff);
}
