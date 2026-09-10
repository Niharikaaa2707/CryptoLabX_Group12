#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <numeric>

using namespace std;

// Standard English letter frequencies (A-Z)
const vector<double> ENGLISH_FREQ = {
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074
};

// Function Declarations
string clean_ciphertext(const string& raw);
map<string, vector<int>> find_repeated_patterns(const string& text, int seq_len = 3);
vector<int> calculate_distances(const map<string, vector<int>>& patterns);
map<int, int> find_factors(const vector<int>& distances);
int kasiski_analysis(const string& text);
double calculate_ic(const string& text);
vector<string> split_into_groups(const string& text, int key_len);
vector<vector<double>> frequency_analysis(const vector<string>& groups);
int find_shift(const string& group);
string find_key(const vector<string>& groups);
string vigenere_decrypt(const string& text, const string& key);
string vigenere_encrypt(const string& text, const string& key);
bool verify(const string& text, const string& key);

// 1. Clean Ciphertext
string clean_ciphertext(const string& raw) {
    string cleaned = "";
    for (char c : raw) {
        if (isalpha(c)) cleaned += toupper(c);
    }
    return cleaned;
}

// 2. Find Repeated Patterns
map<string, vector<int>> find_repeated_patterns(const string& text, int seq_len) {
    map<string, vector<int>> patterns;
    for (size_t i = 0; i <= text.length() - seq_len; ++i) {
        string seq = text.substr(i, seq_len);
        patterns[seq].push_back(i);
    }
    map<string, vector<int>> repeated;
    for (auto& pair : patterns) {
        if (pair.second.size() > 1) {
            repeated[pair.first] = pair.second;
        }
    }
    return repeated;
}

// 3. Calculate Distances
vector<int> calculate_distances(const map<string, vector<int>>& patterns) {
    vector<int> distances;
    for (auto& pair : patterns) {
        const auto& pos = pair.second;
        for (size_t i = 1; i < pos.size(); ++i) {
            distances.push_back(pos[i] - pos[i - 1]);
        }
    }
    return distances;
}

// 4. Find Factors
map<int, int> find_factors(const vector<int>& distances) {
    map<int, int> factor_counts;
    for (int dist : distances) {
        for (int i = 2; i <= 20; ++i) {
            if (dist % i == 0) {
                factor_counts[i]++;
            }
        }
    }
    return factor_counts;
}

// 5. Kasiski Analysis
int kasiski_analysis(const string& text) {
    auto patterns = find_repeated_patterns(text, 3);
    auto distances = calculate_distances(patterns);
    auto factors = find_factors(distances);

    int best_key_len = 3;
    int max_count = 0;
    for (auto& pair : factors) {
        if (pair.second > max_count) {
            max_count = pair.second;
            best_key_len = pair.first;
        }
    }
    return best_key_len;
}

// 6. Calculate Index of Coincidence
double calculate_ic(const string& text) {
    int N = text.length();
    if (N <= 1) return 0.0;
    vector<int> counts(26, 0);
    for (char c : text) counts[c - 'A']++;

    double sum = 0.0;
    for (int count : counts) {
        sum += count * (count - 1);
    }
    return sum / (N * (N - 1));
}

// 7. Split Into Groups
vector<string> split_into_groups(const string& text, int key_len) {
    vector<string> groups(key_len, "");
    for (size_t i = 0; i < text.length(); ++i) {
        groups[i % key_len] += text[i];
    }
    return groups;
}

// 8. Frequency Analysis
vector<vector<double>> frequency_analysis(const vector<string>& groups) {
    vector<vector<double>> freqs;
    for (const string& group : groups) {
        vector<double> group_freq(26, 0.0);
        for (char c : group) group_freq[c - 'A']++;
        for (int i = 0; i < 26; ++i) group_freq[i] /= group.length();
        freqs.push_back(group_freq);
    }
    return freqs;
}

// 9. Find Shift
int find_shift(const string& group) {
    int best_shift = 0;
    double min_chi_sq = 1e9;
    int N = group.length();

    vector<int> counts(26, 0);
    for (char c : group) counts[c - 'A']++;

    for (int g = 0; g < 26; ++g) {
        double chi_sq = 0.0;
        for (int i = 0; i < 26; ++i) {
            double observed = counts[(i + g) % 26];
            double expected = N * ENGLISH_FREQ[i];
            chi_sq += ((observed - expected) * (observed - expected)) / expected;
        }
        if (chi_sq < min_chi_sq) {
            min_chi_sq = chi_sq;
            best_shift = g;
        }
    }
    return best_shift;
}

// 10. Find Key
string find_key(const vector<string>& groups) {
    string key = "";
    for (const string& group : groups) {
        int shift = find_shift(group);
        key += (char)('A' + shift);
    }
    return key;
}

// 11. Vigenere Decrypt
string vigenere_decrypt(const string& text, const string& key) {
    string plaintext = "";
    int key_len = key.length();
    for (size_t i = 0; i < text.length(); ++i) {
        int c = text[i] - 'A';
        int k = key[i % key_len] - 'A';
        char p = (char)('A' + (c - k + 26) % 26);
        plaintext += p;
    }
    return plaintext;
}

// 12. Vigenere Encrypt
string vigenere_encrypt(const string& text, const string& key) {
    string ciphertext = "";
    int key_len = key.length();
    for (size_t i = 0; i < text.length(); ++i) {
        int p = text[i] - 'A';
        int k = key[i % key_len] - 'A';
        char c = (char)('A' + (p + k) % 26);
        ciphertext += c;
    }
    return ciphertext;
}

// 13. Verify Solution
bool verify(const string& text, const string& key) {
    string recovered_pt = vigenere_decrypt(text, key);
    string re_encrypted = vigenere_encrypt(recovered_pt, key);
    return re_encrypted == text;
}

int main() {
    ifstream file("attacks/assignment_6/outputs/ciphertext.txt");
    if (!file.is_open()) {
        cerr << "Error: Could not open ciphertext file!" << endl;
        return 1;
    }
    string raw_input((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();

    string cleaned_ct = clean_ciphertext(raw_input);
    cout << "==========================================" << endl;
    cout << "   VIGENERE CIPHER KASISKI CRYPTANALYSIS   " << endl;
    cout << "==========================================" << endl;
    cout << "Cleaned Ciphertext Length: " << cleaned_ct.length() << " characters\n" << endl;

    int key_len = kasiski_analysis(cleaned_ct);
    cout << "Estimated Key Length (Kasiski Test): " << key_len << endl;

    auto groups = split_into_groups(cleaned_ct, key_len);
    cout << "\nAverage IC across " << key_len << " groups: ";
    double avg_ic = 0.0;
    for (const auto& g : groups) avg_ic += calculate_ic(g);
    cout << fixed << setprecision(4) << (avg_ic / key_len) << " (Expected ~0.065 for English)\n" << endl;

    auto freq_table = frequency_analysis(groups);
    cout << "=== FREQUENCY TABLE FOR EACH GROUP (TOP 3 CHARS) ===" << endl;
    for (size_t g = 0; g < freq_table.size(); ++g) {
        cout << "Group " << (g + 1) << ": ";
        vector<pair<char, double>> sorted_g;
        for (int i = 0; i < 26; ++i) sorted_g.push_back({'A' + i, freq_table[g][i]});
        sort(sorted_g.begin(), sorted_g.end(), [](auto& a, auto& b) { return a.second > b.second; });
        for (int i = 0; i < 3; ++i) {
            cout << sorted_g[i].first << "(" << fixed << setprecision(1) << (sorted_g[i].second * 100) << "%) ";
        }
        cout << endl;
    }

    string recovered_key = find_key(groups);
    cout << "\nRecovered Key: " << recovered_key << endl;

    string recovered_pt = vigenere_decrypt(cleaned_ct, recovered_key);
    cout << "\n=== RECOVERED PLAINTEXT PREVIEW ===" << endl;
    cout << recovered_pt.substr(0, 300) << "...\n" << endl;

    if (verify(cleaned_ct, recovered_key)) {
        cout << "[SUCCESS] Re-encryption verification passed!" << endl;
    } else {
        cout << "[FAILURE] Verification failed!" << endl;
    }

    return 0;
}
