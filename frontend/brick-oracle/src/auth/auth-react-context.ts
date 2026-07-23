import { createContext } from "react";
import type { RouterAuthContext } from "./types";

export const AuthReactContext = createContext<RouterAuthContext | null>(null);
