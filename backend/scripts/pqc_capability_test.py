import oqs


REQUIRED_KEMS = [
    "ML-KEM-512",
    "ML-KEM-768",
    "ML-KEM-1024",
]

REQUIRED_SIGNATURES = [
    "ML-DSA-44",
    "ML-DSA-65",
]


def check_capabilities():
    enabled_kems = set(oqs.get_enabled_kem_mechanisms())
    enabled_signatures = set(oqs.get_enabled_sig_mechanisms())

    print("\n=== PQC CAPABILITY CHECK ===")

    print("\nKEM mechanisms:")
    for algorithm in REQUIRED_KEMS:
        status = "AVAILABLE" if algorithm in enabled_kems else "MISSING"
        print(f"{algorithm}: {status}")

    print("\nSignature mechanisms:")
    for algorithm in REQUIRED_SIGNATURES:
        status = (
            "AVAILABLE"
            if algorithm in enabled_signatures
            else "MISSING"
        )
        print(f"{algorithm}: {status}")

    missing_kems = [
        algorithm
        for algorithm in REQUIRED_KEMS
        if algorithm not in enabled_kems
    ]

    missing_signatures = [
        algorithm
        for algorithm in REQUIRED_SIGNATURES
        if algorithm not in enabled_signatures
    ]

    if missing_kems or missing_signatures:
        print("\nPQC CAPABILITY CHECK FAILED")

        if missing_kems:
            print("Missing KEMs:", missing_kems)

        if missing_signatures:
            print("Missing signatures:", missing_signatures)

        return False

    print("\nPQC CAPABILITY CHECK PASSED")
    return True


if __name__ == "__main__":
    check_capabilities()
