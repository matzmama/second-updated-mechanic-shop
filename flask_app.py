from application import create_app

# 👇 THIS is what Render uses
app = create_app()

# 👇 Only used locally (safe to keep)
if __name__ == "__main__":
    app.run(debug=True)