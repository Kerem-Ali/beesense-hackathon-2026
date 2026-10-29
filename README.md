# BeeSense - Meta Global AI Developer Hackathon 2026
**Track:** Indie Developer | **Theme:** Build for Your World

### What existed BEFORE hackathon (Week 6/10 - DO NOT DEMO)
- Sentinel-2 NDVI pipeline, ERA5-Land, Copernicus DEM, SoilGrids ingestion
- Turkey Bloom Atlas concept, landing page beesense.app, pricing model
- ITU HPC cluster + AMD $2000 credit, Prof Dr Huseyin Toros supervision
- 82,159 forum threads analyzed, 30,923 beekeepers, 52 interviews

### What was built DURING hackathon Oct 27-Nov 4 (THIS REPO - DEMO ONLY THIS)
- **SAM 3.1 Flora Segmentation Engine** - Pine vs Sunflower vs Thyme segmentation from Sentinel-2
- **Llama Spark + Llama Spark Open (Baseten meta-models/llama-spark-open-1026) Agentic Verdict Agent** - 6-layer score + Turkish natural language verdict with tool calling
- **Llama Wonder Route Intelligence v2** - Multi-stop route optimization with reasoning
- **Llama Image Bloom Heatmap** - Visual bloom potential maps for PDF
- **Llama Voice Transcribe** - Voice notes from field in Turkish
- **WhatsApp Cloud API Automation** - Fully automated pin -> PDF flow

### Architecture
User Pin (WhatsApp) -> Cloud API Webhook -> FastAPI -> SAM 3.1 + Scoring Engines -> Llama Spark Open (Baseten) -> Llama Wonder -> Llama Image -> PDF -> WhatsApp

### Meta Models Used
- Llama Spark series (hosted) - Verdict generation
- Llama Wonder - Route reasoning
- Llama Image - Heatmap generation
- SAM 3.1 - Satellite segmentation
- Llama Voice Transcribe - Voice notes
- Llama Spark Open + Llama Glimmer (open-weights via Baseten/Modal)

### Quickstart
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
ngrok http 8000
# Set webhook URL in WhatsApp Cloud API dashboard
```

### Demo Video (3 min)
0-30s: Problem - 104k beekeepers, 18k TL cost, memory/word of mouth
30-90s: Pin on WhatsApp -> SAM 3.1 segmentation -> Llama Spark verdict
90-150s: Route optimization + PDF generation + WhatsApp delivery
150-180s: Impact + scaling to US/EU, Mediterranean expansion
