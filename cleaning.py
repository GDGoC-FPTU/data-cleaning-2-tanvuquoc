import json


def mask_email(email):
    """
    Masks the email address by keeping the first character of the username
    and adding '***' before the domain.

    Example:
    vana@gmail.com -> v***@gmail.com
    """

    if not email or "@" not in email:
        return email

    username, domain = email.split("@", 1)

    if len(username) == 0:
        return "***@" + domain

    return username[0] + "***@" + domain


def clean_data(input_file, output_file):
    # Load the toxic data
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {input_file}.")
        return

    seen_ids = set()
    sanitized_data = []

    for item in data:
        # 1. Deduplication: ensure each id only appears once
        item_id = item.get("id")

        if item_id in seen_ids:
            continue

        # 2. Outlier and sanity check
        price = item.get("price")

        if price is None:
            continue

        if price > 5000:
            continue

        if price < 0:
            continue

        # 3. PII masking
        sanitized_item = item.copy()

        # Remove name field
        sanitized_item.pop("name", None)

        # Mask email field
        if "email" in sanitized_item:
            sanitized_item["email"] = mask_email(sanitized_item["email"])

        # Add to cleaned list and track ID
        sanitized_data.append(sanitized_item)
        seen_ids.add(item_id)

    # Save the sanitized data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sanitized_data, f, indent=4, ensure_ascii=False)

    print(f"Successfully sanitized data. Output saved to {output_file}")
    print(f"Original records: {len(data)}")
    print(f"Sanitized records: {len(sanitized_data)}")


if __name__ == "__main__":
    INPUT_PATH = "toxic_sample.json"
    OUTPUT_PATH = "sanitized_sample.json"
    clean_data(INPUT_PATH, OUTPUT_PATH)