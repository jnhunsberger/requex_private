export class Iris {
    sepalLength: number = 5.0;
    sepalWidth: number = 3.5;
    petalLength: number = 2.5;
    petalWidth: number = 1.2;
}

export class ProbabilityPrediction {
    name: string;
    value: number;
}

export class SVCParameters {
    C: number = 2.0;
}

export class SVCResult {
    accuracy: number;
}

export class CyberLSTMModel {
    modelJSON: string;
    modelH5: string;
}

export class LoadResult {
    returnStatus: string;
}

export class CyberLSTMPredict {
    url: string;
}

export class URLResult {
    url: string;
    type: string;
}
