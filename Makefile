venv: .venv/bin/activate

dev:
	sh -c '. ~/.profile; . .venv/bin/activate && \
		DATABASE_URL='' \
		FLASK_APP=run.py \
		FLASK_DEBUG=1 \
		LC_ALL=C.UTF-8 \
		LANG=C.UTF-8 \
		flask run --host=0.0.0.0 --port=8080'
	