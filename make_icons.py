import argparse
from cairosvg import svg2png
from PIL import Image
from os import path


def define_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser("Create icons for gust")
    p.add_argument(
        "-s",
        "--svg",
        type=str,
        help="File path to the svg file. Must supply either svg or png. Will default to this if multiple things supplied",
        default="",
    )
    p.add_argument(
        "-p",
        "--png",
        type=str,
        help="File path to the svg file. Must supply either svg or png.",
        default="",
    )

    return p


def make_png(fpath: str, size: int, outpath: str):
    out = path.join(outpath, "{:d}.png".format(size))
    print("Making png: {}".format(out))
    svg2png(
        file_obj=open(fpath, "rb"),
        write_to=out,
        output_width=size,
        output_height=size,
    )


def rescale_existing_png(fpath: str, size: int, outpath: str):
    out = path.join(outpath, "{:d}.png".format(size))
    print("Rescaling png: {}".format(out))
    img = Image.open(fpath, 'rb').resize((size, size))
    img.save(out)




if __name__ == "__main__":
    args = define_parser().parse_args()
    sizes = [16, 24, 32, 48, 64]
    linux_size = [128, 256, 512, 1024]
    root_out = "./src/main/icons/"
    base_out = "./src/main/icons/base"
    linux_out = "./src/main/icons/linux"
    mac_out = "./src/main/icons/mac"

    use_svg = False
    if len(args.svg) != 0:
        use_svg = True
        fpath = args.svg
    elif len(args.png) != 0:
        fpath = args.png
    else:
        raise RuntimeError("Must specify either svg or png input file")

    for ii in sizes:
        if use_svg:
            make_png(fpath, ii, base_out)
        else:
            rescale_existing_png(fpath, ii, base_out)

    for ii in linux_size:
        if use_svg:
            make_png(fpath, ii, linux_out)
            make_png(fpath, ii, mac_out)
        else:
            rescale_existing_png(fpath, ii, linux_out)
            rescale_existing_png(fpath, ii, mac_out)

    print("Saving ico")
    img = Image.open(path.join(linux_out, "512.png"))
    img.save(path.join(root_out, "Icon.ico"))