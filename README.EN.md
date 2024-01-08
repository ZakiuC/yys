English | [Simplified Chinese](./README.md)
# Projects
> Yin-Yang Master Monitor Script 
# Version
> V1.0.1


# Structure
> - [static](./static/) - static files
> - [static/images](./static/images/) - images for template matching
> - [grabscreen.py](./grabscreen.py) - windows window content capture
> - [loadModel.py](./loadModel.py) - target image loading for template matching
> - [test.py](./test.py) - test script


# Update log
## V1.0.1 - January 8, 2024
### New
- [Check script run permissions](./test.py#L205-L208)
- [Added keyboard/mouse input simulation](./loadModel.py#L114-L318)
- Class [TargetImage](./loadModel.py#L28-L70) added [click](./loadModel.py#L59-L70) method