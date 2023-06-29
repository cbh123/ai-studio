My new favorite hobby is making trailers for films that don't exist.

Bugsy Shadows — A New York Mystery:

https://github.com/cbh123/ai-studio/assets/14149230/9e34b452-9c47-47bf-a598-22ac600dd68c

Vanderbilt Express by Wes Anderson:

https://github.com/cbh123/ai-studio/assets/14149230/2bb85f46-9b62-49b3-9316-d82116e65379

Planet Zearth narrated by David Ai-ttenborough (skip to 1:40 for the penguin scene):

[Watch Planet Zearth](https://twitter.com/charliebholtz/status/1673466353938776068)

Here's I walkthrough of how I make these AI movies, and how you can too.

## Script
It all starts with the script. Like any good AI filmmaker, I ask ChatGPT for a rough draft. Here's the conversation I had with GPT-4 to create the [David Attenborough clip](https://chat.openai.com/share/95379044-c1c1-4c6f-8141-6381c65d9b3f).

<img width="880" alt="chatgpt_1" src="https://github.com/cbh123/ai-studio/assets/14149230/7f144cba-dfdf-48e0-9df2-6c2a53d4e295">

<img width="893" alt="chatgpt_script" src="https://github.com/cbh123/ai-studio/assets/14149230/4c3dac73-2a3e-4cc9-86bb-c6ada38b3dac">

The script will need a bit of a human touch (I thought it would be funnier if the glow leopard encounters a penguin rather than a fungi). But ChatGPT is a great starting point. 

GPT is really good at silly puns. or at least better than me. Here's a chat I had to create a [Barbie-Oppenheimer crossover](https://chat.openai.com/share/496c8ef0-32c0-442f-bcfd-a5e67575b946)

<img width="869" alt="puns" src="https://github.com/cbh123/ai-studio/assets/14149230/129ba076-94b1-48a9-901a-48f7fff50021">

Note that the AI is good at brainstorming a lot of ideas fast. But many of these scripts are missing something that's hard to put a finger on. That's where us humans come in :)

## Narrator
Phase II — let's bring in a narrator to our production. There are two ways you can do this: the break the terms of service way, and the this is what you're supposed to do way. I shouldn't talk much about the first way, but it may involve finding a YouTube clip of an speaker you like, downloading it as an mp3 using pytube, uploading it into audacity and trimming the best parts, and then uploading to [ElevenLabs](https://beta.elevenlabs.io/voice-lab) voice cloning feature. 

The second way is to use a [community generated voice](https://beta.elevenlabs.io/voice-library), which are pretty good too. I use [[Ixel] Male older American voice, fairly deep too](https://beta.elevenlabs.io/voice-lab/share/4af011ff3556e6d9fa2a801fee549fb5de141c2daab509635a67c1a7c819e15a/VrpwKyFPv8etbiWgnoyA) as a narrator for a few of these videos — he makes a good trailer narrator

<img width="385" alt="ixel" src="https://github.com/cbh123/ai-studio/assets/14149230/537dc6b7-27eb-4e57-8cdf-b825ed51bb63">


## Videos + Music + Editing (the fun part)
Now comes the fun part: making the videos and music, and stitching everything together. Open up iMovie and start a new movie project.

<img width="337" alt="Screenshot 2023-06-29 at 11 40 35 AM" src="https://github.com/cbh123/ai-studio/assets/14149230/0083404e-3f96-4741-ac36-2586c0698638">

Making AI videos is an iterative process. The videos that you create [zeroscope](https://replicate.com/anotherjesse/zeroscope-v2-xl) are amazing, but also weird, so it helps to make a lot of videos and then keep the best ones. I made a Python script that makes this easy. The script creates X number of videos/music for you and then saves the output locally. It all runs in the background. Then you can open up Finder in the directory where the clips are saved and drag the ones you like into iMovie.

Open up a terminal and clone this repo:
```
git clone https://github.com/cbh123/ai-studio
cd ai-studio
```

Install Replicate:
```
pip install replicate
export REPLICATE_API_TOKEN=<your-token>
```
If you don't have an API token, you can create a Replicate account [here](https://replicate.com/accounts/billing).

Optionally, change the `PROJECT_NAME` on line 7 in `main.py` to a project name of your choice. This tells ai studio where to save your output.

Now, you can run the script with this command, and the prompts will save to the ai-studio/videos/<project-name> directory:

`python main.py "prompt for your content" <number-of-outputs> --type <video/music> --style <a-style-that-you-want-appended-to-all-videos> &`

For example, here's how to create 3 videos of a glowing leopard:

```
python main.py "bioluminescent leopards walking in the forest" 3 --type video --style "national geographic, 4k &"
```

> I always add a `&` to the end of the command so that it runs in the background. This way you can send off a bunch of
> different requests to Replicate without having to open up new terminals or wait for the predictions to finish. To see
> progress, you can run `tail -F studio.log` to tail the logs (quit with `ctrl+c`)

As for the kinds of prompts you should use to create videos with——you're going to need a bit of trial and error. But to get started, let's ask our AI friend. This GPT-4 prompt works decently well (in the same chat where you created the script):

```
I want to create a series of videos to make this trailer, and I'd like your help describing what the videos should look like for my text-to-video model. Can you describe all the videos I'll need to create as if you were sending it as a prompt to a text-to-video model?

Some rules:
- the text-to-video model only makes videos with no sound. so no need to describe the sound
- If the video features a character, can you describe them? instead of saying names, describe the character. Remember, this text-to-video model doesn't know who the characters are.
- NO NAMES! Just describe the character. Don't say "John", say "a man in a suit"
- Don't say action verbs. Just describe in plain detail what's in the video
```

<img width="834" alt="example_t2v_prompts" src="https://github.com/cbh123/ai-studio/assets/14149230/591fa31c-61f5-4766-a000-6ef8556a32ed">

This is a decent starting off point, but I'd encourage you to experiment with the prompts and styles. My friend [fofrAI](https://twitter.com/fofrAI) got my started with the following parameters for zeroscope, but feel free to play with these too. 

```
{
  num_frames: 24, # zeroscrope struggles with higher values here
  fps: 12, # 2s videos
  width: 576,
  height: 320,
  guidance_scale: 12.5,
  num_inference_steps: 50,
  model: '576w',
  negative_prompt: 'noisy, washed out, ugly, distorted, low quality, garish',
  prompt: '<your-prompt>'
}
```

So now my workflow looks like a lot of this:

> "Hmmm, I want to see a shot of a family before we show individual characters"

Run:
```
python main.py "a family wearing fancy clothes in a palatial room" --style "wide angle, wes anderson, colorful" --type video 3 &
```

> Then I decided that the "disillusioned inventor, Augustus" needed to be frustrated with his progress creating the worlds quietest blender:

```
python main.py "a man in a suit, frustrated, hands on head" --style "wes anderson, colorful" --type video 2 &
```

Creating the music is a similar process. Instead of `--type video`, it's `--type music`. Also note that `--style` doesn't do anything for music generation.

Here's the prompt I used for the Wes Anderson trailer:
```
python main.py "upbeat, classical music" --type music 2 &
```

Now that we have a nice selection of narration, video clips, and music, it's a matter of dragging into iMovie and iterating from there. This process looks a lot like this. A lot of dragging, dropping, shuffling, and then creating new videos and repeating:

https://github.com/cbh123/ai-studio/assets/14149230/5bf32837-1cea-4761-a351-d5ba9443f93c

I like this trick that fades out the sound:

https://github.com/cbh123/ai-studio/assets/14149230/f6b349be-83f5-4902-89a9-77a1333f65fb

Can't wait to see what you make!

## Tips:
- The `--style` is helpful for keeping a consistent, um, style. I'd play with [prompter](https://prompter.fofr.ai/) to find some styles that might fit. Some styles I've had success with:
  - macro
  - film noir
  - black and white
  - wes anderson
  - national geographic
  - deep ocean
- Generally I run 2-3 minimum videos per generation. The results can be off sometimes, so it's nice to be able to pick the best ones to drag into iMovie.
- Don't forget the `&` at the end of the command! This makes the python script run in the background.
- Within VSCode, the alt+cmd+R shortcut is really nice for opening up the content before pulling into iMovie. Example:

https://github.com/cbh123/ai-studio/assets/14149230/01f3b692-d4b2-4782-a665-46ce565c783c






