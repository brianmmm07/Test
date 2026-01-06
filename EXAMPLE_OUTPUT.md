# Example Output: Running the arXiv Paper Summarizer

This is an example of what you'll see when running `python main.py` with the new features.

```bash
$ python main.py

============================================================
arXiv Paper Summarizer - 2026-01-06 14:30:45
============================================================

Initializing components...
Verifying Notion connection...
Connected to Notion database: 1a2b3c4d5e6f7g8h9i0j

Searching for papers in 2 categories:
  - Image Generation: image generation, diffusion model, image editing
  - Video Generation: video generation, video extension, motion synthesis

Searching arXiv for 'image generation' (Category: Image Generation)
Searching arXiv for 'diffusion model' (Category: Image Generation)
Searching arXiv for 'image editing' (Category: Image Generation)
Searching arXiv for 'video generation' (Category: Video Generation)
Searching arXiv for 'video extension' (Category: Video Generation)
Searching arXiv for 'motion synthesis' (Category: Video Generation)
Found 12 papers total

Processing 12 papers...

Loading existing papers from database for similarity matching...
Found 47 existing papers in database

[1/12] Processing: DreamEdit: Subject-Driven Image Editing via Diffusion-Based...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - InstructPix2Pix: Learning to Follow Image Editing In... (similarity: 0.782)
    - Prompt-to-Prompt Image Editing with Cross Attention C... (similarity: 0.756)
    - DiffEdit: Diffusion-based Semantic Image Editing via... (similarity: 0.743)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: DreamEdit: Subject-Driven Image Editing via Dif...
  Saving to local database...
  ✓ Complete

[2/12] Processing: VideoComposer: Compositional Video Synthesis with Motion...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - AnimateDiff: Animate Your Personalized Text-to-Image... (similarity: 0.801)
    - Gen-2: Multi-Modal Video Generation from Text and Ima... (similarity: 0.779)
    - I2VGen-XL: High-Quality Image-to-Video Synthesis via... (similarity: 0.754)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: VideoComposer: Compositional Video Synthesis wit...
  Saving to local database...
  ✓ Complete

[3/12] Processing: Consistent4D: Consistent 360° Dynamic Object Generation...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - DreamGaussian: Generative Gaussian Splatting for Eff... (similarity: 0.698)
    - Zero-1-to-3: Zero-shot One Image to 3D Object... (similarity: 0.672)
    - Magic3D: High-Resolution Text-to-3D Content Creation... (similarity: 0.654)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: Consistent4D: Consistent 360° Dynamic Object Gen...
  Saving to local database...
  ✓ Complete

[4/12] Processing: PALP: Prompt Aligned Personalization of Text-to-Image Mo...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - DreamBooth: Fine Tuning Text-to-Image Diffusion Mode... (similarity: 0.823)
    - Custom Diffusion: Multi-Concept Customization of Text... (similarity: 0.798)
    - LoRA: Low-Rank Adaptation of Large Language Models... (similarity: 0.712)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: PALP: Prompt Aligned Personalization of Text-to-...
  Saving to local database...
  ✓ Complete

[5/12] Processing: MotionCtrl: A Unified and Flexible Motion Controller for...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - AnimateDiff: Animate Your Personalized Text-to-Image... (similarity: 0.765)
    - VideoComposer: Compositional Video Synthesis with Mot... (similarity: 0.743)
    - ControlNet: Adding Conditional Control to Text-to-Im... (similarity: 0.721)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: MotionCtrl: A Unified and Flexible Motion Control...
  Saving to local database...
  ✓ Complete

[6/12] Processing: StreamDiffusion: A Pipeline-level Solution for Real-Time...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - Latent Consistency Models: Synthesizing High-Resolut... (similarity: 0.787)
    - SDXL Turbo: Adversarial Diffusion Distillation... (similarity: 0.756)
    - Stable Diffusion XL: Improving Latent Diffusion Mode... (similarity: 0.734)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: StreamDiffusion: A Pipeline-level Solution for R...
  Saving to local database...
  ✓ Complete

[7/12] Processing: EMO: Emote Portrait Alive - Generating Expressive Portra...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - SadTalker: Learning Realistic 3D Motion Coefficients... (similarity: 0.812)
    - Wav2Lip: Accurately Lip-syncing Videos In The Wild... (similarity: 0.778)
    - GAIA: Zero-shot Talking Avatar Generation... (similarity: 0.743)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: EMO: Emote Portrait Alive - Generating Expressive...
  Saving to local database...
  ✓ Complete

[8/12] Processing: FlowVid: Taming Imperfect Optical Flows for Consistent V...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - CoDeF: Content Deformation Fields for Temporally Con... (similarity: 0.789)
    - TokenFlow: Consistent Diffusion Features for Consist... (similarity: 0.767)
    - Rerender A Video: Zero-Shot Text-Guided Video-to-Vid... (similarity: 0.745)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: FlowVid: Taming Imperfect Optical Flows for Cons...
  Saving to local database...
  ✓ Complete

[9/12] Processing: InstructVideo: Instructing Video Diffusion Models with H...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - InstructPix2Pix: Learning to Follow Image Editing In... (similarity: 0.734)
    - Text2Video-Zero: Text-to-Image Diffusion Models are... (similarity: 0.712)
    - Tune-A-Video: One-Shot Tuning of Image Diffusion Mod... (similarity: 0.698)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: InstructVideo: Instructing Video Diffusion Models...
  Saving to local database...
  ✓ Complete

[10/12] Processing: MagicAnimate: Temporally Consistent Human Image Animati...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - AnimateAnyone: Consistent and Controllable Image-to-... (similarity: 0.856)
    - DreamPose: Fashion Image-to-Video Synthesis via Stab... (similarity: 0.823)
    - DisCo: Disentangled Control for Referring Human Danc... (similarity: 0.791)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: MagicAnimate: Temporally Consistent Human Image A...
  Saving to local database...
  ✓ Complete

[11/12] Processing: PhotoMaker: Customizing Realistic Human Photos via Stac...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - InstantID: Zero-shot Identity-Preserving Generation... (similarity: 0.834)
    - IP-Adapter: Text Compatible Image Prompt Adapter for... (similarity: 0.801)
    - FaceStudio: Put Your Face Everywhere in Seconds... (similarity: 0.776)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: PhotoMaker: Customizing Realistic Human Photos vi...
  Saving to local database...
  ✓ Complete

[12/12] Processing: PixArt-δ: Fast and Controllable Image Generation with L...
  Computing paper embedding...
  Finding similar papers...
  Found 5 similar papers:
    - PixArt-α: Fast Training of Diffusion Transformer for... (similarity: 0.912)
    - SDXL: Improving Latent Diffusion Models for High-Res... (similarity: 0.798)
    - DiT: Scalable Diffusion Models with Transformers... (similarity: 0.765)
  Generating AI summary...
  Creating markdown with related papers...
  Adding to Notion...
Added paper to Notion: PixArt-δ: Fast and Controllable Image Generation...
  Saving to local database...
  ✓ Complete

============================================================
Processing Summary:
  - Papers added: 12
  - Papers failed: 0
============================================================

Database Statistics:
  - Total papers: 59
  - Papers by category:
    * Image Generation: 32
    * Video Generation: 27
  - Date range: 2023-11-15 to 2026-01-06
  - Similarity connections: 142
============================================================
```

## Example of Related Papers in Notion

Here's what you'd see in a Notion page for one of the papers:

---

# DreamEdit: Subject-Driven Image Editing via Diffusion-Based Generation

**Authors:** Wei Xiong, Yuxuan Zhang, Qingnan Fan, Junhao Zhu, Bo Dai

**Published:** 2026-01-05

**Category:** Image Generation

**arXiv Category:** cs.CV

**Search Keyword:** image editing

**PDF:** [http://arxiv.org/abs/2401.12345](http://arxiv.org/abs/2401.12345)

---

## Overview
DreamEdit presents a novel framework for subject-driven image editing that combines diffusion models with precise control mechanisms. The method enables users to edit specific subjects within images while maintaining consistency with the surrounding context.

## Key Contributions
- Introduces a dual-branch architecture separating subject and background generation
- Achieves 23% improvement in editing quality over baseline methods
- Demonstrates zero-shot generalization to unseen subjects
- Enables fine-grained control through natural language instructions
- Maintains temporal consistency in sequential edits

## Methodology
The approach uses a pre-trained diffusion model with specialized attention mechanisms. Subject encoding is performed through a novel embedding technique that preserves identity while allowing flexible modifications.

## Potential Impact
This work could significantly advance personalized content creation, enabling more intuitive and powerful image editing tools for both professionals and consumers.

---

## 🔗 Related Papers

Based on content similarity, here are the most related papers:

1. **InstructPix2Pix: Learning to Follow Image Editing Instructions**
   - Authors: Tim Brooks, Aleksander Holynski, Alexei A. Efros
   - Published: 2022-11-17
   - Similarity: 78%
   - [PDF](https://arxiv.org/pdf/2211.09800.pdf)

2. **Prompt-to-Prompt Image Editing with Cross Attention Control**
   - Authors: Amir Hertz, Ron Mokady et al.
   - Published: 2022-08-02
   - Similarity: 76%
   - [PDF](https://arxiv.org/pdf/2208.01626.pdf)

3. **DiffEdit: Diffusion-based Semantic Image Editing via Mask Guidance**
   - Authors: Guillaume Couairon, Jakob Verbeek et al.
   - Published: 2022-10-20
   - Similarity: 74%
   - [PDF](https://arxiv.org/pdf/2210.11427.pdf)

4. **ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models**
   - Authors: Lvmin Zhang, Maneesh Agrawala
   - Published: 2023-02-10
   - Similarity: 68%
   - [PDF](https://arxiv.org/pdf/2302.05543.pdf)

5. **DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation**
   - Authors: Nataniel Ruiz, Yuanzhen Li et al.
   - Published: 2022-08-25
   - Similarity: 65%
   - [PDF](https://arxiv.org/pdf/2208.12242.pdf)

---

*Summary generated by Claude AI*

---

## Example of Using the Search Tool

```bash
# Search for papers by a specific author
$ python search.py --author "Jiaming Song"

======================================================================
Title: DreamEdit: Subject-Driven Image Editing via Diffusion-Based Generation
Authors: Wei Xiong, Yuxuan Zhang, Jiaming Song
Published: 2026-01-05
Category: Image Generation
PDF: http://arxiv.org/abs/2401.12345

======================================================================
Title: Denoising Diffusion Implicit Models
Authors: Jiaming Song, Chenlin Meng, Stefano Ermon
Published: 2020-10-06
Category: Image Generation
PDF: http://arxiv.org/abs/2010.02502

# Show database statistics
$ python search.py --stats

======================================================================
DATABASE STATISTICS
======================================================================

Total Papers: 59

Papers by Category:
  - Image Generation: 32
  - Video Generation: 27

Date Range:
  - Earliest: 2023-11-15
  - Latest: 2026-01-06

Similarity Connections: 142
======================================================================

# Find papers similar to a specific one
$ python search.py --similar "2401.12345"

Finding papers similar to:
======================================================================
Title: DreamEdit: Subject-Driven Image Editing via Diffusion-Based Generation
Authors: Wei Xiong, Yuxuan Zhang, Jiaming Song
Published: 2026-01-05
Category: Image Generation
PDF: http://arxiv.org/abs/2401.12345

Abstract:
DreamEdit presents a novel framework for subject-driven image editing...

Top 10 most similar papers:

1. Similarity: 78%
======================================================================
Title: InstructPix2Pix: Learning to Follow Image Editing Instructions
Authors: Tim Brooks, Aleksander Holynski, Alexei A. Efros
Published: 2022-11-17
Category: Image Generation
PDF: https://arxiv.org/abs/2211.09800
```

This shows the complete workflow with all the new features working together!
