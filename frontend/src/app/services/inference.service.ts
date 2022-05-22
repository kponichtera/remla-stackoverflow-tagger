import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

export interface PredictionResult {
  title: string,
  result: string[],
  classifier: string,
}

export interface PredictionCorrectionRequest {
  title: string,
  predicted: string[],
  actual: string[],
}

@Injectable({
  providedIn: 'root'
})
export class InferenceService {

  constructor(private http: HttpClient) { }

  ping(): Observable<any> {
    return this.http.get('api/ping');
  }

  predict(title: string): Observable<PredictionResult> {
    return this.http.post<PredictionResult>('api/predict', title);
  }

  correctPrediction(request: PredictionCorrectionRequest): Observable<any> {
    return this.http.post('api/predict', request);
  }

}
