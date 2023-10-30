#pragma once

#include <vector>
#include <regex>
#include <algorithm>

#include <model_meta.hpp>

class TglangPreprocessor
{
    const size_t max_string_len = 4096;

    /**
     * Shift all encoded lines to the left by the minimum number of leading spaces.
     */
    std::vector<std::vector<det_int_t>> shift_lines_left(std::vector<std::vector<det_int_t>> &lines)
    {
        int min_leading_spaces = INT32_MAX;

        for (const auto &line : lines)
        {
            int count = 0;
            for (auto token : line)
            {
                if (token >= SPACES_RANGE[0] && token <= SPACES_RANGE[1])
                    count++;
                else
                    break;
            }
            min_leading_spaces = std::min(min_leading_spaces, count);
        }

        if (min_leading_spaces == 0 || min_leading_spaces == INT32_MAX)
            return lines;

        for (auto &line : lines)
        {
            if (min_leading_spaces < line.size())
                line.erase(line.begin(), line.begin() + min_leading_spaces);
            else
                line.clear();
        }

        return lines;
    }

    /**
     * Join encoded lines into a single vector, removing empty lines.
     */
    std::vector<det_int_t> joinlines(std::vector<std::vector<det_int_t>> &lines)
    {
        std::vector<det_int_t> encoded_text;

        auto lines_ = shift_lines_left(lines);

        for (size_t i = 0; i < lines_.size(); i++)
        {
            for (auto v : lines_[i])
                encoded_text.push_back(v);
            if (i != lines_.size() - 1)
                encoded_text.push_back(VOCAB_NEW_LINE_ID);
        }
        return encoded_text;
    }

    /**
     * Get the first non-space character in an encoded line.
     */
    det_int_t get_starting_char(std::vector<det_int_t> &mline)
    {
        for (auto v : mline)
            if (v < SPACES_RANGE[0] || v > SPACES_RANGE[1])
                return v;
        return -1;
    }

    /**
     * Remove lines which start with the same character excluding leading spaces.
     */
    std::vector<std::vector<det_int_t>> remove_duplicate_starting(std::vector<std::vector<det_int_t>> &lines)
    {
        size_t total_len = 0;
        for (const auto &line : lines)
            total_len += line.size() + 1;

        det_int_t last_val = -1;
        std::vector<std::vector<det_int_t>> filtered_lines;

        size_t line_id = 0;
        for (; line_id < lines.size(); line_id++)
        {
            det_int_t start_char = get_starting_char(lines[line_id]);

            if ((start_char != -1 && start_char != last_val) || start_char == VOCAB_UNK_ID)
                filtered_lines.push_back(lines[line_id]);
            else
                total_len -= lines[line_id].size() + 1;

            if (total_len <= MODEL_MAX_INPUT)
                break;

            last_val = start_char;
        }

        for (size_t i = line_id + 1; i < lines.size(); i++)
            filtered_lines.push_back(lines[i]);

        return filtered_lines;
    }

    /**
     * Remove or cut lines if the total length of the encoded text is greater than MODEL_MAX_INPUT.
     */
    std::vector<det_int_t> filter_encoded(std::vector<det_int_t> &encoded_text)
    {
        if (encoded_text.size() <= MODEL_MAX_INPUT)
            return encoded_text;

        std::vector<std::vector<det_int_t>> lines;
        std::vector<det_int_t> cur_line;
        for (auto v : encoded_text)
        {
            if (v == VOCAB_NEW_LINE_ID)
            {
                lines.push_back(cur_line);
                cur_line.clear();
            }
            else
                cur_line.push_back(v);
        }
        if (!cur_line.empty())
            lines.push_back(cur_line);

        size_t total_len = 0;
        for (const auto &line : lines)
            total_len += line.size() + 1;

        int left_per_line = std::max(MAX_LINE_LEN, (int)(total_len / lines.size()));

        for (size_t i = 0; i < lines.size(); i++)
        {
            if (lines[i].size() > left_per_line)
            {
                size_t rem_len = lines[i].size() - left_per_line;

                lines[i].resize(left_per_line);
                total_len -= rem_len;

                if (total_len <= MODEL_MAX_INPUT)
                    return joinlines(lines);
            }
        }

        auto filtered_lines = remove_duplicate_starting(lines);
        return joinlines(filtered_lines);
    }

    /**
     * Debug function to print encoded data.
     */
    void print_data(const std::string &s, std::vector<det_int_t> &data)
    {
        std::cout << "### SOURCE  ###: " << std::endl;
        std::cout << s << std::endl;
        std::cout << "### DECODED ###: " << std::endl;
        for (auto v : data)
            std::cout << vocab_list[v];
        std::cout << std::endl;
    }

    /**
     * Count the number of leading spaces in a string.
     */
    size_t count_leading_spaces(const std::string &s)
    {
        size_t count = 0;
        for (char char_ : s)
        {
            if (char_ == ' ' || char_ == '\t')
                count++;
            else
                break;
        }
        return count;
    }

    void rstrip(std::string &s)
    {
        size_t end = s.find_last_not_of(" \t");
        if (end != std::string::npos)
            s.resize(end + 1);
        else
            s.clear();
    }

    /**
     * Remove quoted text.
     */
    std::string remove_quoted_text(const std::string &s)
    {
        std::regex double_quoted_pattern(R"(\"([^"]*)\")");
        std::regex single_quoted_pattern(R"('([^']*)')");

        std::string result = std::regex_replace(s, double_quoted_pattern, R"("")");
        result = std::regex_replace(result, single_quoted_pattern, R"('')");

        return result;
    }

    /**
     * Remove continuous tokens which correspond to [a-zA-Z0-9_] and replace them with <UNK>.
     */
    std::vector<det_int_t> replace_continuous(const std::vector<det_int_t> &nums, int range_start, det_int_t N)
    {
        std::vector<det_int_t> new_list;
        new_list.reserve(nums.size());

        int i = 0;
        while (i < nums.size())
        {
            if (range_start <= nums[i])
            {
                new_list.push_back(N);
                while (i < nums.size() && range_start <= nums[i])
                    i++;
            }
            else
            {
                new_list.push_back(nums[i]);
                i++;
            }
        }
        return new_list;
    }

    /**
     * Convert text to tokens.
     */
    std::vector<det_int_t> encode_text(const std::string &inptext)
    {
        std::string text = inptext;
        std::transform(text.begin(), text.end(), text.begin(), ::tolower);

        std::vector<det_int_t> encoded_text;
        encoded_text.reserve(text.size());

        auto i = text.begin();
        while (i != text.end())
        {
            bool found = false;
            auto end = i + std::min(VOCAB_MAX_LEN, static_cast<int>(text.end() - i));
            for (auto j = end; j != i; --j)
            {
                if (vocab_map.find({i, j}) != vocab_map.end())
                {
                    encoded_text.push_back(vocab_map.at({i, j}));
                    i = j;
                    found = true;
                    break;
                }
            }
            if (!found)
            {
                encoded_text.push_back((det_int_t)VOCAB_UNK_ID);
                ++i;
            }
        }

        encoded_text = replace_continuous(encoded_text, LETTERS_POSE, (det_int_t)VOCAB_UNK_ID);

        return encoded_text;
    }

    /**
     * Convert text to string and preprocess it:
     *  - remove the minimum number of leading spaces
     *  - remove spaces and tabs at the end of each line
     *  - remove empty lines
     *  - remove quoted text
     */
    std::string arrange_text(const char *text)
    {
        std::string raw(text, std::min(this->max_string_len, strlen(text)));

        std::istringstream stream(raw);
        std::string line;
        std::vector<std::string> lines;

        while (std::getline(stream, line))
            lines.push_back(line);

        size_t min_leading = SIZE_MAX;
        for (const auto &line : lines)
            if (!line.empty() && line.find_first_not_of(" \t") != std::string::npos)
                min_leading = std::min(min_leading, count_leading_spaces(line));

        std::string result;
        for (size_t i = 0; i < lines.size(); ++i)
        {
            if (!lines[i].empty() && lines[i].find_first_not_of(" \t") != std::string::npos)
            {
                lines[i] = lines[i].substr(min_leading);
                rstrip(lines[i]);
                result += lines[i];
                if (i != lines.size() - 1)
                    result += "\n";
            }
        }

        result = remove_quoted_text(result);

        return result;
    }

public:
    std::vector<det_int_t> preprocess(const char *text)
    {
        std::string text_str = arrange_text(text);

        if (text_str.empty())
            return {};

        std::vector<det_int_t> encoded_text = encode_text(text_str);
        std::vector<det_int_t> input_data = filter_encoded(encoded_text);

        if (input_data.size() > MODEL_MAX_INPUT)
            input_data.resize(MODEL_MAX_INPUT);

        return input_data;
    }
};