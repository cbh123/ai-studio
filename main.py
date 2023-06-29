import os
import argparse
import replicate
from urllib.request import urlretrieve
import logging

PROJECT_NAME = "project"

logging.basicConfig(
    filename="studio.log",  # Specify the file name for logging
    level=logging.DEBUG,  # Set the desired logging level
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def music(prompt, num_outputs):
    # make music with musicgen https://replicate.com/joehoover/musicgen
    model = replicate.models.get("joehoover/musicgen")
    version = model.versions.get(
        "f8578df960c345df7bc1f85dd152c5ae0b57ce45a6fc09511c467a62ad820ba3"
    )
    input = {"prompt": prompt, "duration": 28}
    return main(version, input, num_outputs, "music")


def video(prompt, num_outputs, style=None):
    # make videos with zeroscope https://replicate.com/anotherjesse/zeroscope-v2-xl
    model = replicate.models.get("anotherjesse/zeroscope-v2-xl")
    version = model.versions.get(
        "1f0dd155aeff719af56f4a2e516c7f7d4c91a38c7b8e9e81808e7c71bde9b868"
    )
    input = {
        "prompt": prompt + (f", {style}" if style else ""),
        "negative_prompt": "noisy, washed out, ugly, distorted, broken",
        "num_frames": 24,
        "width": 1024,
        "height": 576,
        "guidance_scale": 17.5,
        "fps": 12,
    }

    return main(version, input, num_outputs, "videos")


def main(version, input, num_outputs, folder):
    all_predictions = create_predictions(version, input, num_outputs)
    download_path = download_predictions(all_predictions, folder)
    logging.info(f"Downloaded outputs(s) to {download_path}")
    return


def create_predictions(version, input, num_outputs):
    all_predictions = []

    for i in range(num_outputs):
        video_prediction = replicate.predictions.create(
            version=version,
            input=input,
        )
        all_predictions.append(video_prediction)

    done = False

    while not done:
        [p.reload() for p in all_predictions]
        for p in all_predictions:
            logging.info(f"https://replicate.com/p/{p.id} \n {p.logs}")
        done = all_done(all_predictions)

    logging.info("Predictions complete")
    return all_predictions


def download_predictions(predictions, folder):
    script_directory = os.path.dirname(os.path.abspath(__name__))
    download_path = os.path.join(script_directory, folder, PROJECT_NAME)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for p in predictions:
        if type(p.output) == str:
            url = p.output
        elif type(p.output) == list:
            url = p.output[0]

        filetype = url.split(".")[-1]
        name = p.input["prompt"] + f"_{p.id}_" + f".{filetype}"
        local_filename = os.path.join(download_path, name)
        urlretrieve(url, local_filename)

    return download_path


def all_done(predictions):
    return set([p.status for p in predictions]) == {"succeeded"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper for generating movies.")
    parser.add_argument("prompt", type=str, help="prompt")
    parser.add_argument("num_output", type=int, help="# outputs")
    parser.add_argument("--type", type=str, help="video/music/sound", default="video")
    parser.add_argument("--style", type=str, help="optional global style", default=None)

    args = parser.parse_args()

    if args.type == "music":
        music(args.prompt, args.num_output)
    elif args.type == "video":
        video(args.prompt, args.num_output, args.style)
    else:
        print("Invalid type")
