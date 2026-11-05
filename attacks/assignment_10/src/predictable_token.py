import random
import time


TOKEN_LENGTH = 16
SEARCH_WINDOW = 300


def generate_token(timestamp):
    generator = random.Random(timestamp)
    token = bytearray()

    for i in range(TOKEN_LENGTH):
        token.append(generator.getrandbits(8))

    return bytes(token)


def predict_timestamp(observed_token, start_timestamp, end_timestamp):
    tested = 0
    matches = []

    for candidate_timestamp in range(start_timestamp, end_timestamp + 1):
        tested += 1
        candidate_token = generate_token(candidate_timestamp)

        if candidate_token == observed_token:
            matches.append(candidate_timestamp)

    return tested, matches


def demonstrate_token_attack():
    timestamp = int(time.time())
    token = generate_token(timestamp)

    start_timestamp = timestamp - SEARCH_WINDOW
    end_timestamp = timestamp + SEARCH_WINDOW

    print("\nPART B: PREDICTABLE PASSWORD RESET TOKEN")
    print("Generation timestamp :", timestamp)
    print("Observed token (hex) :", token.hex())
    print("Search interval      :", start_timestamp, "to", end_timestamp)

    tested, matches = predict_timestamp(
        token, start_timestamp, end_timestamp
    )

    print("Timestamps tested    :", tested)
    print("Matching timestamps  :", matches)

    if len(matches) == 1:
        recovered_timestamp = matches[0]
        regenerated_token = generate_token(recovered_timestamp)

        print("Recovered timestamp  :", recovered_timestamp)
        print("Timestamp is correct :", recovered_timestamp == timestamp)
        print("Regenerated token    :", regenerated_token.hex())
        print("Token verification  :", regenerated_token == token)


if __name__ == "__main__":
    demonstrate_token_attack()
