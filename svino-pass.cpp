#include <maxminddb.h>
#include <cstring>
#include <iostream>

extern "C" {
    MMDB_s mmdb;
    bool is_db_loaded = false;

    int init_db(const char* db_path) {
        int status = MMDB_open(db_path, MMDB_MODE_MMAP, &mmdb);
        if (status == MMDB_SUCCESS) {
            is_db_loaded = true;
            return 1;
        }
        return 0; 
    }

    void close_db() {
        if (is_db_loaded) {
            MMDB_close(&mmdb);
            is_db_loaded = false;
        }
    }

    int get_country_by_ip(const char* ip_address, char* output_buffer, int max_len) {
        if (!is_db_loaded) return 0;

        int gai_error, mmdb_error;
        MMDB_lookup_result_s result = MMDB_lookup_string(&mmdb, ip_address, &gai_error, &mmdb_error);

        if (gai_error != 0 || mmdb_error != MMDB_SUCCESS || !result.found_entry) {
            return 0; 
        }

        MMDB_entry_data_s entry_data;
        int status = MMDB_get_value(&result.entry, &entry_data, "country", "names", "en", NULL);

        if (status == MMDB_SUCCESS && entry_data.has_data && entry_data.type == MMDB_DATA_TYPE_UTF8_STRING) {
            int len = entry_data.data_size < (max_len - 1) ? entry_data.data_size : (max_len - 1);
            strncpy(output_buffer, entry_data.utf8_string, len);
            output_buffer[len] = '\0';
            return 1;
        }
        return 0;
    }
}