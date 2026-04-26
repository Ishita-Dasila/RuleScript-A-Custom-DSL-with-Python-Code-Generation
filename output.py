def check_age(age):
    """Auto-generated rule: check_age"""
    if age >= 18:
        eligible = True
    else:
        eligible = False
    return eligible

def check_score(score):
    """Auto-generated rule: check_score"""
    if score >= 50:
        result = True
    else:
        result = False
    return result

def check_admin(level):
    """Auto-generated rule: check_admin"""
    if level >= 5:
        is_admin = True
    return is_admin

def check_discount(purchase):
    """Auto-generated rule: check_discount"""
    if purchase >= 1000:
        discount = True
    else:
        discount = False
    return discount

def check_driving(age):
    """Auto-generated rule: check_driving"""
    if age >= 16:
        can_drive = True
    else:
        can_drive = False
    return can_drive


# ── Quick demo (run this file directly) ────────
if __name__ == "__main__":
    print("=== RuleScript Generated Code — Demo ===")
    result = check_age(18)
    print(f"  check_age(age=18) => {result}")
    result = check_score(18)
    print(f"  check_score(score=18) => {result}")
    result = check_admin(18)
    print(f"  check_admin(level=18) => {result}")
    result = check_discount(18)
    print(f"  check_discount(purchase=18) => {result}")
    result = check_driving(18)
    print(f"  check_driving(age=18) => {result}")
