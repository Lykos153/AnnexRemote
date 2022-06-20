{
  description = "Flake to setup python virtualenv with direnv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: 
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in rec {
      packages = {
        pythonEnv = pkgs.python3.withPackages(
          ps: with ps; [
            virtualenv
          ]
        );
      };

      defaultPackage = packages.pythonEnv;
      devShell = packages.pythonEnv.env;
    });
}
