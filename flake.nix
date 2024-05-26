{
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... }@inputs:
    with inputs;
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      nativeBuildInputs = with pkgs; [
        gup
        shellcheck
      ];

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
        ]));

      tools = with pkgs;
        doc-tools ++ [ nasm python-tools ];
    in {
      hydraJobs = { inherit (self) packages; };

      devShells.${system}.default = pkgs.mkShell {
        inherit buildInputs;
        nativeBuildInputs = nativeBuildInputs ++ tools;
      };
}
