# PASS PowerPoint → Anki workflow

This automation converts a PASS `.ppt` or `.pptx` into atomic text cards, image-recognition cards, and one-target masked image-occlusion cards.

## Activate the workflow

The workflow source is stored at `workflow-templates/generate-pass-anki.yml`. Copy it unchanged to `.github/workflows/generate-pass-anki.yml` on the default branch. GitHub integrations often cannot create workflow files unless granted a separate Workflows permission, so this final copy may need to be made in GitHub's web editor.

## One-time secret setup

1. Open **Settings → Secrets and variables → Actions**.
2. Choose **New repository secret**.
3. Name it `OPENAI_API_KEY`.
4. Paste the API key as the value and save it.
5. Never put the key in a workflow input or committed file.

## Supply a deck

Use exactly one method:

- **Repo path:** Upload the deck to a private branch or an `inputs/` folder and provide a path such as `inputs/clotting.ppt`. This is easiest, but the deck remains in Git history unless purged.
- **Direct URL:** Supply a direct HTTPS download URL and set `deck_filename` to the correct `.ppt` or `.pptx` filename. A normal sharing webpage is not a direct download URL.

## Run it

1. Open **Actions**.
2. Select **Generate PASS Anki cards**.
3. Choose **Run workflow**.
4. Fill either `deck_path` or `deck_url`.
5. Keep the default model and batch size initially.
6. Run the workflow.
7. Download `pass-anki-N` from the run's **Artifacts** section.

## Import into Anki

1. Unzip the artifact.
2. Copy everything inside `media/` into Anki's `collection.media` directory.
3. Import `cards.tsv` with **Tab** as the separator.
4. Map columns to **Front**, **Back**, and **Tags**.
5. Enable HTML in fields.

The masked-image cards follow Image Occlusion Enhanced principles but import as portable image-backed notes; the add-on is not required.

## Outputs

- `cards.tsv`: Anki import file.
- `cards.txt`: readable `Front | Back | Tags` version.
- `media/`: source-slide images and one-answer masked images.
- `review_rejects.txt`: malformed cards and unmatched occlusion targets.
- `extracted_slides.txt`: slide-text audit trail.

Review medical accuracy before studying. Source decks may contain outdated or internally inconsistent claims.
