import os
import sys
from pathlib import Path


pardir = Path(__file__).parent.parent.as_posix()
sys.path.append(os.path.join(pardir, "src"))
import main  # noqa E402
from log import setup_logger  # noqa E402


def test_main(monkeypatch, tmp_path, mock_config_file, mock_mysql):

    f = tmp_path/"tmp.sendmail.txt"
    fn = f.as_posix()
    print()
    print(f"tmp_file={fn}")

    def mock_create_logger(*args, **kwargs):
        return setup_logger("test")

    def mock_sendmail(_, email, body, attachment=None):
        with open(fn, "a") as fh:
            fh.write(f"{email}, {body}, {attachment}\n")

        return email, body, attachment

    monkeypatch.setattr(main, "create_logger", mock_create_logger)
    monkeypatch.setattr(main, "sendmail", mock_sendmail)

    os.environ["DB_CONFIG"] = mock_config_file

    mock_mysql.result = [
        {"ct": 2, "first_name": "John", "last_name": "Doe", "email": "johndoe@abc.com"},
        {"ct": 2, "first_name": "Jane", "last_name": "Doe", "email": "janedoe@xyz.com"},
    ]

    if os.path.exists(fn):
        os.remove(fn)

    main.main()

    exp_results = [
        "John Doe <johndoe@abc.com>, Welcome John, please enjoy this week's newsletter and our special discount offer., discount_offer.pdf\n",  # noqa E501
        "Jane Doe <janedoe@xyz.com>, Welcome Jane, please enjoy this week's newsletter and our special discount offer., discount_offer.pdf\n",  # noqa E501
        "John Doe <johndoe@abc.com>, Welcome John, please enjoy this week's newsletter., None\n",
        "Jane Doe <janedoe@xyz.com>, Welcome Jane, please enjoy this week's newsletter., None\n",
    ]

    idx = 0
    with open(fn, "r") as fh:
        for line in fh:
            assert line == exp_results[idx]
            idx += 1
            print(f"{line=}")
