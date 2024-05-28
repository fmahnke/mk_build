{
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... }@inputs:
    with inputs;
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonPkgs = pkgs.python311.pkgs;

      nativeBuildInputs = with pkgs; [ gup shellcheck ];

      buildInputs = [ ];

      doc-tools = with pkgs; [ graphviz plantuml ];

      python-tools = (pkgs.python3.withPackages (python-pkgs:
        with python-pkgs; [
          autopep8
          coverage
          python-lsp-server
          flake8
          jedi
          mypy
          nox
          pylsp-mypy
          pytest
          rope
          tomlkit
        ]));

      tools = with pkgs; doc-tools ++ [ nasm python-tools ];
    in {
      packages.x86_64-linux.default = pythonPkgs.buildPythonPackage {
        pname = "mk_build";
        version = "0.1.0";
        pyproject = true;

        src = ./python-project;

        buildInputs = with pythonPkgs; [ tomlkit setuptools ];

        propagatedBuildInputs = with pythonPkgs; [ pytest tomlkit ];
      };

      hydraJobs = { inherit (self) packages; };

      devShells.${system}.default = pkgs.mkShell {
        inherit buildInputs;
        nativeBuildInputs = nativeBuildInputs ++ tools;
      };
    };
}
