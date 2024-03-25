import * as React from "react"
import { StaticImage } from "gatsby-plugin-image"

export default function Logo() {
  return (
  <StaticImage className="logo" src="https://raw.githubusercontent.com/HenriquesLab/DL4MicEverywhere/main/docs/logo/dl4miceverywhere-logo-small.png" alt="catalog logo" placeholder="blurred" fit="contain"/>
  );
}