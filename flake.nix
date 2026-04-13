{
  description = "kp: knowledge pipeline (GitHub -> AI -> Obsidian + Anki)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
          ];

          shellHook = ''
            export UV_PYTHON_DOWNLOADS=never

            if [ ! -d .venv ]; then
              uv venv --python ${python}/bin/python
            fi

            source .venv/bin/activate
          '';
        };
      });
}
