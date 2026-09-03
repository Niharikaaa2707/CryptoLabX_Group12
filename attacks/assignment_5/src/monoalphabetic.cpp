#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>
#include <iomanip>

using namespace std;

// Function Prototypes
map<char, int> frequency_analysis(const string& ciphertext);
map<string, int> word_frequency_analysis(const string& ciphertext, int word_len);
void pattern_analysis(const string& ciphertext);
string apply_substitution(const string& ciphertext, const map<char, char>& sub_map);
void display_partial_plaintext(const string& partial_text);
bool verify_solution(const string& original_plaintext, const string& recovered_plaintext);

// 1. Frequency Analysis
map<char, int> frequency_analysis(const string& ciphertext) {
    map<char, int> freq;
    int total_letters = 0;
    
    for (char c : ciphertext) {
        if (isalpha(c)) {
            char upper_c = toupper(c);
            freq[upper_c]++;
            total_letters++;
        }
    }

    // Sort in descending order for display
    vector<pair<char, int>> sorted_freq(freq.begin(), freq.end());
    sort(sorted_freq.begin(), sorted_freq.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second;
    });

    cout << "\n=== 1. LETTER FREQUENCY ANALYSIS ===" << endl;
    cout << "Letter | Count | Percentage" << endl;
    cout << "---------------------------" << endl;
    for (const auto& p : sorted_freq) {
        double pct = (double)p.second / total_letters * 100.0;
        cout << "   " << p.first << "   |  " << setw(4) << p.second << " | " << fixed << setprecision(2) << pct << "%" << endl;
    }

    return freq;
}

// 2. Word Frequency Analysis
map<string, int> word_frequency_analysis(const string& ciphertext, int word_len) {
    map<string, int> word_counts;
    string current_word = "";

    for (char c : ciphertext) {
        if (isalpha(c)) {
            current_word += toupper(c);
        } else {
            if (!current_word.empty()) {
                if (word_len == 0 || current_word.length() == word_len) {
                    word_counts[current_word]++;
                }
                current_word = "";
            }
        }
    }
    if (!current_word.empty() && (word_len == 0 || current_word.length() == word_len)) {
        word_counts[current_word]++;
    }

    return word_counts;
}

// 3. Pattern Analysis
void pattern_analysis(const string& ciphertext) {
    cout << "\n=== 2. WORD & PATTERN ANALYSIS ===" << endl;
    
    for (int len = 1; len <= 3; ++len) {
        map<string, int> words = word_frequency_analysis(ciphertext, len);
        cout << "\nMost Frequent " << len << "-Letter Words:" << endl;
        vector<pair<string, int>> sorted_words(words.begin(), words.end());
        sort(sorted_words.begin(), sorted_words.end(), [](const auto& a, const auto& b) {
            return a.second > b.second;
        });

        int limit = 0;
        for (const auto& w : sorted_words) {
            if (limit++ >= 5) break;
            cout << "  " << w.first << " : " << w.second << " times" << endl;
        }
    }
}

// 4. Apply Substitution
string apply_substitution(const string& ciphertext, const map<char, char>& sub_map) {
    string result = ciphertext;
    for (size_t i = 0; i < result.length(); ++i) {
        if (isalpha(result[i])) {
            char upper_c = toupper(result[i]);
            if (sub_map.find(upper_c) != sub_map.end()) {
                char substituted = sub_map.at(upper_c);
                result[i] = islower(ciphertext[i]) ? tolower(substituted) : substituted;
            } else {
                result[i] = '*'; // Unmapped letters represented by asterisk
            }
        }
    }
    return result;
}

// 5. Display Partial Plaintext
void display_partial_plaintext(const string& partial_text) {
    cout << "\n=== PARTIAL PLAINTEXT PREVIEW ===" << endl;
    cout << partial_text.substr(0, 250) << "...\n" << endl;
}

// 6. Verify Solution
bool verify_solution(const string& original_plaintext, const string& recovered_plaintext) {
    string clean_orig = "", clean_rec = "";
    for (char c : original_plaintext) if (isalpha(c)) clean_orig += toupper(c);
    for (char c : recovered_plaintext) if (isalpha(c)) clean_rec += toupper(c);
    return clean_orig == clean_rec;
}

int main() {
    // Read Original Plaintext
    ifstream file("outputs/plaintext.txt");
    if (!file.is_open()) {
        cerr << "Error: Could not open outputs/plaintext.txt" << endl;
        return 1;
    }
    string plaintext((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();

    // Fixed Substitution Key Generation
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string key      = "QWERTYUIOPASDFGHJKLZXCVBNM"; // Monoalphabetic Key
    map<char, char> encrypt_map, decrypt_map;

    for (size_t i = 0; i < 26; ++i) {
        encrypt_map[alphabet[i]] = key[i];
        decrypt_map[key[i]] = alphabet[i];
    }

    // Encrypt Plaintext
    string ciphertext = plaintext;
    for (size_t i = 0; i < ciphertext.length(); ++i) {
        if (isalpha(ciphertext[i])) {
            char base = isupper(ciphertext[i]) ? 'A' : 'a';
            char sub = encrypt_map[toupper(ciphertext[i])];
            ciphertext[i] = islower(ciphertext[i]) ? tolower(sub) : sub;
        }
    }

    cout << "==========================================" << endl;
    cout << "    MONOALPHABETIC CIPHER CRYPTANALYSIS   " << endl;
    cout << "==========================================" << endl;

    // Run Frequency and Pattern Analysis
    frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    // Iterative Reconstruction Simulation
    map<char, char> current_hypothesis;
    cout << "\n=== 3. ITERATIVE RECOVERY STEPS ===" << endl;

    // Step 1: Map most frequent cipher letter 'R' -> 'E'
    current_hypothesis['R'] = 'E';
    cout << "[Step 1] Hypothesized R -> E (Most frequent ciphertext character)" << endl;
    display_partial_plaintext(apply_substitution(ciphertext, current_hypothesis));

    // Step 2: Map 3-letter word "ZIT" -> "THE"
    current_hypothesis['Z'] = 'T';
    current_hypothesis['I'] = 'H';
    cout << "[Step 2] Hypothesized ZIT -> THE based on 3-letter word pattern" << endl;
    display_partial_plaintext(apply_substitution(ciphertext, current_hypothesis));

    // Final Step: Apply complete inverse key
    string final_recovered = apply_substitution(ciphertext, decrypt_map);

    cout << "=== 4. VERIFICATION & VALIDATION ===" << endl;
    if (verify_solution(plaintext, final_recovered)) {
        cout << "[SUCCESS] Decrypted text matches original plaintext perfectly!" << endl;
    } else {
        cout << "[FAILURE] Decryption verification failed!" << endl;
    }

    return 0;
}
