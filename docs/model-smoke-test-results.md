# Hosted Model Smoke-Test Results

**Status:** Smoke tests passed on GitHub-hosted Ubuntu CPU runners on 22 October 2026.

## Results

| Model / implementation | Test image | Detections reported | First-prediction time |
|---|---|---:|---:|
| YOLOv8n (yolov8n.pt) | Public Ultralytics bus demo | 6 | 1,629.69 ms |
| YOLO11n (yolo11n.pt) | Public Ultralytics bus demo | 5 | 175.05 ms |
| YOLO26n (yolo26n.pt) | Public Ultralytics bus demo | 5 | 179.49 ms |
| LibreYOLO RT-DETR (LibreRTDETRr18.pt) | Public Ultralytics bus demo | 7 | 316.17 ms |

## Workflow evidence

- [YOLOv8 / YOLO11 / YOLO26 hosted run](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39699180838)
- [LibreYOLO RT-DETR hosted run](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39699357117)
- [Repository CI run](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39699357153)

## Interpretation and limitations

These runs establish that the selected model implementations downloaded and completed generic object-detection inference on a hosted CPU runner. The image contains a bus and people, **not coconuts**.

- These results are not a coconut-detection benchmark and do not demonstrate coconut precision, recall, maturity classification, orchard generalization, or robot-harvesting capability.
- The reported times include the first prediction and are not a controlled latency comparison. Hardware, initialization, library overhead, and model implementation differ.
- Detection counts are not an accuracy score and must not be used to rank the models.
- The LibreYOLO RT-DETR run is an initial candidate for a more permissively licensed stack. Before commercial redistribution, verify the exact code, pretrained checkpoint, dependencies, and notices against their upstream licenses.
- No model has been selected as the production coconut detector based on these smoke tests alone.

## Next evaluation

1. Build or curate a coconut image dataset with documented provenance and labels.
2. Use a fixed train/validation/test split and keep test images out of training.
3. Fine-tune compatible candidate models on the training split.
4. Report precision, recall, mAP@0.50, mAP@0.50:0.95, model size, and controlled latency on the same hardware.
5. Review licenses before selecting a model for commercial deployment.

This report records an engineering smoke test, not a claim of a validated agricultural AI system.
