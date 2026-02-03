{
  description = "Tabgrounds: Python backend + React frontend";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Backend (Python)
            python314
            uv
            ruff
            ty
            
            # Frontend (React/Bun)
            bun

            # General Tools
            git
            honcho
            just
            prek
          ];

          shellHook = ''
            uv sync --all-groups --project ./backend
            bun install --dev --cwd ./frontend
            prek install

            echo "Welcome to the Tabgrounds development environment!"
          '';
        };
      }
    );
}
