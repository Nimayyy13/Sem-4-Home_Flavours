import os

def configure_password():
    print("🔧 MySQL Password Configuration")
    print("=" * 40)
    print("Please enter your MySQL root password:")
    password = input("Password:sanskruti14")
    
    # Read existing .env file
    env_lines = []
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_lines = f.readlines()
    
    # Update or add DB_PASSWORD
    password_updated = False
    new_lines = []
    
    for line in env_lines:
        if line.startswith('DB_PASSWORD='):
            new_lines.append(f'DB_PASSWORD={password}\n')
            password_updated = True
        else:
            new_lines.append(line)
    
    if not password_updated:
        new_lines.append(f'DB_PASSWORD={password}\n')
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.writelines(new_lines)
    
    print("✅ Password configured successfully!")
    print("You can now test the connection with: python test_mysql.py")

if __name__ == "__main__":
    configure_password() 