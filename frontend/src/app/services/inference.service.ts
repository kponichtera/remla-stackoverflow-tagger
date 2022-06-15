import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

export interface PredictionRequest {
  title: string,
}

export interface PredictionResult {
  title: string,
  tags: string[],
  classifier: string,
}

export interface CorrectionRequest {
  title: string,
  predicted: string[],
  actual: string[],
}

@Injectable({
  providedIn: 'root'
})
export class InferenceService {

  constructor(private http: HttpClient) { }

  checkModelPresence(): Observable<boolean> {
    return this.http.get<boolean>('api/model_present');
  }

  predict(request: PredictionRequest): Observable<PredictionResult> {
    return this.http.post<PredictionResult>('api/predict', request);
  }

  correctPrediction(request: CorrectionRequest): Observable<any> {
    return this.http.post('api/correct', request);
  }

}
